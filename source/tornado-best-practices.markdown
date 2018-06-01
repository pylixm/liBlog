---
layout : post
title : 我心中的 tornado 最佳实践
category : tornado
date : 2017-03-10 20:00:00
tags : [tornado, best_practices ]
---

最新开发新项目一直在学习tornado的知识，在前人的基础上找了些最佳实践，记录如下，备查。

tornado 新人一枚，欢迎大神拍砖~ 

## 项目目录结构

```python
import tornado.ioloop
import tornado.web

## 业务处理层
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

## 系统入口app 及 路由层
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```
上边是tornado 官网的hello world的实例，tornado做为web框架使用时，只需要处理逻辑的handler和系统入口application及路由即可启动系统，只提供了框架
最核心的部分，使系统更加灵活。这样我们在开发的时候便拥有了自主选择权，可以选择自己喜欢的模板语言，可以选择是否使用orm，根据自己的需求任意组装。
这样问题便来了，我们只能凭借我们有限的开发经验来组织我们的项目结构，路由层、业务层、数据库层等。有没有一个tornado的项目结构的最佳实践呢？
经同事介绍，我从github 上找到了这个项目[tornado-boilerplate](https://github.com/bueda/tornado-boilerplate),虽说6年没有更新了，但是这个目录结构对
我这个初学者足够了。

```
tornado-boilerplate/
    handlers/  # handler 处理逻辑
        foo.py
        base.py  # 在其中重写 RequestHandler 的部分方法，或自定义方法完成自己的功能。
    lib/  # 其他python的模块 
    logconfig/  # 日志相关配置
    media/  # 静态文件
        css/
            vendor/
        js/
            vendor/
        images/
    requirements/  # 环境依赖
        common.txt
        dev.txt
        production.txt
    templates/  # 模板文件
    vendor/  # python的依赖包
    environment.py  # 修改python path 增加 lib vender等目录的包
    fabfile.py  # 远程部署文件
    app.py  # app 启动文件
    settings.py  # 项目配置文件 
```

## sqlalchemy 和 tornado的结合

sqlalchemy 是python系用的最多的orm，我们的项目也选用了sqlalchemy 。在结合sqlalchemy 和tornado过程中，查阅了大量资料。
sqlalchemy 执行各种操作时，最基本的单元为session。sqlalchemy 官方文档建议，尽量适用框架的第三方扩展包来集成sqlalchemy，可以自动的管理session范围。根据sqlalchemy 文档，session的管理放在了每次的request请求中处理为最佳，及每次请求进来时，实例化session，请求结束后，将session关闭，见[这里](http://docs.sqlalchemy.org/en/latest/orm/contextual.html#using-thread-local-scope-with-web-applications)和 [tornado的一个相关issues](https://github.com/tornadoweb/tornado/issues/1675)。

结合如下：

```python
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *  # import the engine to bind
# engine = create_engine(connect_str, pool_size=1, pool_recycle=3600, echo=False, max_overflow=10, echo_pool=True)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/users", UsersHandler),
        ]
        settings = dict(
            cookie_secret="some_long_secret_and_other_settins"
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        # Have one global connection.
        self.session = scoped_session(sessionmaker(bind=engine))

class BaseHandler(tornado.web.RequestHandler):

	def prepare(self):
        self.session = self.application.session

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.query(User).get(user_id)
	
	def on_finish(self):
		self.session.remove()
```

此处的scoped_session, 可理解为session的注册表，从中取用和交还，并保证多次取用的为统一session。详见官方文档，[这里](http://docs.sqlalchemy.org/en/latest/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session)

另外需要注意，此处的sqlalchemy的数据库查询，并不是异步，当使用tornado 的异步特性时，遇到查询数据库慢时，还是会阻塞的，此时我们更多的需要考虑的
是去优化我们的sql，而不是异步查询数据库。因为，当数据库的查询慢到可以阻塞进程时，说明确实是有问题了。除非我们确实是有这种长时间查询数据库的需求。
tornado 本身并没有提供数据库层的异步，看了许多异步查询数据库的三方库，都不是特别成熟。还有另一种解决方案，是使用其他异步任务库来完成长时间查询数据库的

需求，如celery。

**update 2017-05-03**

1、tornado 本身还提供了一种通用的异步解决方案，即使用线程池的方式，见官方文档[这里](http://www.tornadoweb.org/en/stable/faq.html#why-isn-t-this-example-with-time-sleep-running-in-parallel)。
总结下来，实现异步有3中方式：
- 使用gen方式
- 使用线程池方式
- 使用第3放库方式

2、如上结合tornado 和sqlalchemy 时，所有的资源都是tornado进程独有的。例如，在application中生成的session。

3、`pool_size`为进程池常驻进程数量，等到回收时间到时回收。 `max_overflow` 为最大超出`pool_size`的链接数量，此链接可以被`remove`回收。得出以上结论依据如下：
- 在连续请求的情况下，数据库链接不断上升，达到最大值后，有可能报 `TimeoutError: QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30`。原因如下：
    - scoped_session 每次请求尝试新的session（推断，有待验证）
    - 老的session被占用
- 将`pool_size` 和 `max_overflow`的值互换后，以上错误没有出现，且链接池链接数量有减少的情况。    


## tornado 日志使用

tornado 的日志模块使用了python的logging模块实现。tornado 文档日志部分说的比较简单，[这里](http://www.tornadoweb.org/en/stable/log.html).
让人读了，比较糊涂，文中说了，3个内部的 logger: `access` 、`application` 和 `general`。一开始我以为是使用这3个logger来记录tornado中的日志信息，
其实不是，他们只是tornado自己内部使用的。我们完全可以自己获取我们的logger,即使用root logger 。tornado 作者建议如此，可见[这里](https://groups.google.com/forum/#!topic/python-tornado/QSKNn4_l0Oo)

可如下使用，在py中直接获取logger:
```python 
import logging 

logger = logging.getLogger(__name__)

logger.info('...')
```

同时tornado提供了，logger的配置项，提供了日志的文件的命名，路径，切分等功能。均在在`tornado.log.py`里定义。

```python
# tornado/log.py 
def define_logging_options(options=None):
    """Add logging-related flags to ``options``.

    These options are present automatically on the default options instance;
    this method is only necessary if you have created your own `.OptionParser`.

    .. versionadded:: 4.2
        This function existed in prior versions but was broken and undocumented until 4.2.
    """
    if options is None:
        # late import to prevent cycle
        import tornado.options
        options = tornado.options.options
    options.define("logging", default="info",
                   help=("Set the Python log level. If 'none', tornado won't touch the "
                         "logging configuration."),
                   metavar="debug|info|warning|error|none")
    options.define("log_to_stderr", type=bool, default=None,
                   help=("Send log output to stderr (colorized if possible). "
                         "By default use stderr if --log_file_prefix is not set and "
                         "no other logging is configured."))
    options.define("log_file_prefix", type=str, default=None, metavar="PATH",
                   help=("Path prefix for log files. "
                         "Note that if you are running multiple tornado processes, "
                         "log_file_prefix must be different for each of them (e.g. "
                         "include the port number)"))
    options.define("log_file_max_size", type=int, default=100 * 1000 * 1000,
                   help="max size of log files before rollover")
    options.define("log_file_num_backups", type=int, default=10,
                   help="number of log files to keep")

    options.define("log_rotate_when", type=str, default='midnight',
                   help=("specify the type of TimedRotatingFileHandler interval "
                         "other options:('S', 'M', 'H', 'D', 'W0'-'W6')"))
    options.define("log_rotate_interval", type=int, default=1,
                   help="The interval value of timed rotating")

    options.define("log_rotate_mode", type=str, default='size',
                   help="The mode of rotating files(time or size)")

    options.add_parse_callback(lambda: enable_pretty_logging(options))

```
当`parse_command_line()`执行时，日志默认值被初始化，通知格式化了root logger，相关代码均在`tornado.log.py`中。

有关root logger 的理解，可阅读这篇博客[《python日志logging详解》](https://my.oschina.net/leejun2005/blog/126713)

如何修改tornado日志格式，可参考这里，[change the log outpu format for a tornado app](http://stackoverflow.com/questions/30764666/can-you-change-the-log-output-format-for-a-tornado-app)


## 其他找到的最佳实践的资料

- [tornado wiki](https://github.com/tornadoweb/tornado/wiki/Deployment) 你可以从tornado的wiki找到一些生产和开发中的最佳实践。

- [Intoduction tornado](http://demo.pythoner.com/itt2zh/) 虽然此文档的tornado版本是老的，但是介绍的知识点，比较全面且通俗易懂。

>todo 持续更新


