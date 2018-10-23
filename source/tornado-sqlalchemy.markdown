---
layout : post
title : SQLAlchemy 数据库链接池问题排查记录
category : tornado
date : 2017-08-29
tags : [tornado, sqlalchemy]
---


## 环境

web框架：tornado 4.4.2
ORM： SQLAlchemy 1.2.0b1
DB: MySQL 5.7
<!-- more -->
## 问题描述

我们的项目为tornado 开发的API服务，使用SQLALchemy 作为ORM与数据库做交互，SQLAlchemy我们使用了链接池的方式。代码如下：
```python
connect_str = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (settings.get("user"), settings.get("password"),
                                                    settings.get("host"), settings.get("port"), settings.get("name"))
engine = create_engine(connect_str, pool_size=10, pool_recycle=300, echo=False, max_overflow=5)
```

在线上运行中，我们发现每隔一段时间会报数据库链接的错误，错误日志如下：
```
    Traceback (most recent call last):
      File "/usr/local/myapi/env/lib/python3.6/site-packages/sqlalchemy/pool.py", line 687, in _finalize_fairy
        fairy._reset(pool)
      File "/usr/local/myapi/env/lib/python3.6/site-packages/sqlalchemy/pool.py", line 827, in _reset
        self._reset_agent.rollback()
      File "/usr/local/myapi/env/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 1612, in rollback
        self._do_rollback()
      File "/usr/local/myapi/env/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 1650, in _do_rollback
        self.connection._rollback_impl()
      File "/usr/local/myapi/env/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 703, in _rollback_impl
        self._handle_dbapi_exception(e, None, None, None, None)
      File "/usr/local/myapi/env/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 1393, in _handle_dbapi_exception
        exc_info
      File "/usr/local/myapi/env/lib/python3.6/site-packages/sqlalchemy/util/compat.py", line 203, in raise_from_cause
        reraise(type(exception), exception, tb=exc_tb, cause=cause)
      File "/usr/local/myapi/env/lib/python3.6/site-packages/sqlalchemy/util/compat.py", line 186, in reraise
        raise value.with_traceback(tb)
      File "/usr/local/myapi/env/lib/python3.6/site-packages/sqlalchemy/engine/base.py", line 701, in _rollback_impl
        self.engine.dialect.do_rollback(self.connection)
      File "/usr/local/myapi/env/lib/python3.6/site-packages/sqlalchemy/dialects/mysql/base.py", line 1572, in do_rollback
        dbapi_connection.rollback()
      File "/usr/local/myapi/env/lib/python3.6/site-packages/pymysql/connections.py", line 788, in rollback
        self._execute_command(COMMAND.COM_QUERY, "ROLLBACK")
      File "/usr/local/myapi/env/lib/python3.6/site-packages/pymysql/connections.py", line 1088, in _execute_command
        self._write_bytes(packet)
      File "/usr/local/myapi/env/lib/python3.6/site-packages/pymysql/connections.py", line 1040, in _write_bytes
        "MySQL server has gone away (%r)" % (e,))
    sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2006, "MySQL server has gone away (BrokenPipeError(32, 'Broken pipe'))")
```
或如下错误：
```
(pymysql.err.OperationalError) (2014, 'Command Out of Sync')
```

## 分析过程

1、根据错误，怀疑是SQLAlchemy 链接池回收的问题。通过阅读链接池的官方文档, 看到如下描述：
>Above, any DBAPI connection that has been open for more than one hour will be invalidated and replaced, upon next checkout. Note that the invalidation only occurs during checkout - not on any connections that are held in a checked out state. pool_recycle is a function of the Pool itself, independent of whether or not an Engine is in use.

[这里](http://docs.sqlalchemy.org/en/latest/core/pooling.html?highlight=pool_recycle#setting-pool-recycle)

可知，链接的回收并不会导致正在被使用的链接的异常。

将回收时间调小测试，确实并没有引起以上的报错。


2、根据错误信息查询，发现github社区有人遇到同样的报错，是因为mysql数据库的数据包太大导致，见[这里](https://github.com/PyMySQL/PyMySQL/issues/426)。后来`pymysql`的维护者，针对此问题做了修正。查看我们数据的参数 `max_allowed_packet`足够大，所以也不回一切上边的报错。pymysql 默认这个值为 16M([这里](http://pymysql.readthedocs.io/en/latest/modules/connections.html?highlight=max_allowed_packet)),也足够大。

3、查询stackoverflow, 发下如下问题：[Python SQLAlchemy - “MySQL server has gone away”](https://stackoverflow.com/questions/18054224/python-sqlalchemy-mysql-server-has-gone-away)。按照此解决方法，增加链接池的监听函数，代码如下：
```python
def checkout_listener(dbapi_con, con_record, con_proxy):
    try:
        try:
            dbapi_con.ping(False)
        except TypeError:
            dbapi_con.ping()
    except dbapi_con.OperationalError as exc:
        if exc.args[0] in (2006, 2013, 2014, 2045, 2055):
            raise DisconnectionError()
        else:
            raise

event.listen(engine, 'checkout', checkout_listener)
```
代码解读：
1、使用SQLAlchemy 的`PoolListener`监听链接池的可用性，
2、在链接被`checkout`使用时，先验证链接的有效性，若无效则抛出`DisconnectionError`错误，让链接池回收，重新创建个新的链接。

更多SQLAlchemy无效链接的描述，见[官方文档](http://docs.sqlalchemy.org/en/latest/core/pooling.html#dealing-with-disconnects)

4、增加链接池监听函数后也是不见好转。便通过日志打印，跟踪了session 的分配和回收过程，`发现在tornado 的多进程异步模式下，多进程获取的session 并不是主进程的session,而是从连接池中获取的新的session，而这个session,并没有关闭操作，主进程中 `on_finish` 函数中的`remove`只能交还主进程中的session`。看到这里，恍然大悟，非阻塞进程获取的新的session,长期没有交还连接池，导致session超时，mysql 自动断开连接。在非阻塞进程中，增加交还session的代码后解决问题。



## 参考

- [https://discorporate.us/jek/talks/SQLAlchemy-EuroPython2010.pdf](https://discorporate.us/jek/talks/SQLAlchemy-EuroPython2010.pdf)
- [SQLAlchemy无效链接描述](http://docs.sqlalchemy.org/en/latest/core/pooling.html#dealing-with-disconnects)
- [SQLALchemy事件描述](http://docs.sqlalchemy.org/en/latest/core/pooling.html#pool-events)