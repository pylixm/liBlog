---
layout : post
title : python的MySQLdb模块 连接 mysql 错误
category : mysql
date : 2016-03-08
tags : [mysql,]
---


### Q & A：

今天在使用python直接链接数据库时报错 `_mysql_exceptions.OperationalError: (2002, "Can't connect to local MySQL server through socket '/var/lib/mysql/mysql.sock' (2)")`

代码：

    db = MySQLdb.connect(host='localhost',
                         port=3306,
                         user='root',
                         passwd='root',
                         db='mydb')
                     
错误：
    
    Traceback (most recent call last):
      File "./data_db.py", line 5, in < module>
        db='mydb')
      File "/usr/local/env/lib/python2.7/site-packages/MySQLdb/__init__.py", line 81, in Connect
      File "/usr/local/env/lib/python2.7/site-packages/MySQLdb/connections.py", line 187, in __init__
    _mysql_exceptions.OperationalError: (2002, "Can't connect to local MySQL server through socket '/var/lib/mysql/mysql.sock' (2)")

### 原因：

从网上查找原因找到如下描述：

因为我们连接mysql的时候，host用的是localhost, 实际用的是UNIX Domain Socket（具体见参考文献(1)）来进行通信的。

我们知道，UNIX Domain Socket的地址是一个socket类型的文件在文件系统中的路径，如果这个路径不存在的话，连接的时候就会失败。

上面提示的错误原因是”Can’t connect to local MySQL server through socket ‘/var/lib/mysql/mysql.sock’ (2)”，

从字面意思上来看，是说无法通过’/var/lib/mysql/mysql.sock’这个socket来连接本地的mysql sever，这时候问题基本就比较明显了，

应该是mysql配置的本地连接的socket不是’/var/lib/mysql/mysql.sock’这个路径的原因。


### 解决方案：

（1）在python MySQLdb连接的时候，指定所用的unix_socket

    db = MySQLdb.connect(host='localhost',
                         port=3306,
                         user='root',
                         passwd='root',
                         db='mydb',
                         unix_socket='/tmp/mysql.sock')
                         
（2）修改本地mysql server的UNIX Domain Socket

    # The following options will be passed to all MySQL clients
    [client]
    #password       = your_password
    port            = 3306
    socket          = /var/lib/mysql/mysql.sock
     
    # The MySQL server
    [mysqld]
    bind-address = your ip
    port            = 3306
    socket          = /var/lib/mysql/mysql.sock
    
（3）修改本地mysql server支持远程访问（具体见参考文献(2)），采用普通socket进行连接

db = MySQLdb.connect(host='your ip',
                     port=3306,
                     user='root',
                     passwd='root',
                     db='mysite')
                     
                     
#### 参考

* [http://www.wuzesheng.com/?p=2234](http://www.wuzesheng.com/?p=2234)