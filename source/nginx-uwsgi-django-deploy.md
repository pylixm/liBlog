---
layout : post
title : nginx+uwsgi 发布django项目常遇到的问题
category : django
date : 2018-09-11
tags : [django, nginx, uwsgi]
---


nginx + uwsgi +django 是一种比较常见的django部署方式了，除了此种方式还有使用gunicorn来代替uwsgi的，gunicorn可以开启协程模式，有兴趣的可以去看gunicorn的文档，此处不做探讨。本文主要总结收集了nginx+uwsgi方式部署时长遇到的问题。
<!-- more -->
nginx server配置：

```nginx
#tream component nginx needs to connect to
upstream djangostream {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}

# configuration of the server
server {
    # the port your site will be served on
    listen      80;
    # the domain name it will serve for
    server_name localhost; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste
    large_client_header_buffers 4 16k;

    # Django media
    location /media  {
        alias /you/path/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /you/path/staticfiles; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        #uwsgi_pass  127.0.0.1:8001; # or no use upstream  
        uwsgi_pass  djangostream;
        include     /usr/local/nginx/conf/uwsgi_params; # the uwsgi_params file you installed
    }
}

```

uwsgi 部署模板：

```
[uwsgi]
socket = 0.0.0.0:8002
# the base directory (full path)
chdir = /opt/myweb
wsgi-file = /opt/myweb/wsgi.py
processes = 4
threads = 2
buffer-size=32768
stats = 127.0.0.1:9191
daemonize=/opt/myweb/web.log
# clear environment on exit
vacuum = true

# 常用配置说明：
# socket ： 地址和端口号，例如：socket = 127.0.0.1:50000
# processes ： 开启的进程数量
# workers ： 开启的进程数量，等同于processes（官网的说法是spawn the specified number of  workers / processes）
# chdir ： 指定运行目录（chdir to specified directory before apps loading）
# wsgi-file ： 载入wsgi-file（load .wsgi file）
# stats ： 在指定的地址上，开启状态服务（enable the stats server on the specified address）
# threads ： 运行线程。（run each worker in prethreaded mode with the specified number of threads）
# master ： 允许主进程存在（enable master process）
# daemonize ： 使进程在后台运行，并将日志打到指定的日志文件或者udp服务器（daemonize uWSGI）。实际上最常用的，还是把运行记录输出到一个本地文件上。
# log-maxsize ：以固定的文件大小（单位KB），切割日志文件。 例如：log-maxsize = 50000000  就是50M一个日志文件。
# pidfile ： 指定pid文件的位置，记录主进程的pid号。
# vacuum ： 当服务器退出的时候自动清理环境，删除unix socket文件和pid文件（try to remove all of the generated file/sockets）
# disable-logging ： 不记录请求信息的日志。只记录错误以及uWSGI内部消息到日志中。如果不开启这项，那么你的日志中会大量出现这种记录：
# [pid: 347|app: 0|req: 106/367] 117.116.122.172 () {52 vars in 961 bytes} [Thu Jul  7 19:20:56 2016] POST /post => generated 65 bytes in 6 msecs (HTTP/1.1 200) 2 headers in 88 bytes (1 switches on core 0)
# log-maxsize: 日志大小，当大于这个大小会进行切分 (Byte)
# log-truncate: 当启动时切分日志
```

## 常见问题收集

**1、WSGI/uwsgi/uWSGI区别**

- WSGI是一种通信协议。
- uwsgi是一种线路协议而不是通信协议，在此常用于在uWSGI服务器与其他网络服务器的数据通信。
- 而uWSGI是实现了uwsgi和WSGI两种协议的Web服务器。

可以通过`pip list`看到我们按照的uWSGI:

```
uWSGI                     2.0.17.1
```

**2、nignx与后端uwsgi链接问题**

nignx error日志如下：

```
2018/09/04 16:21:24 [error] 22660#0: *1 connect() failed (111: Connection refused) while connecting to upstream, client: 10.222.76.194, server: localhost, request: "GET /favicon.ico HTTP/1.1", upstream: "uwsgi://127.0.0.1:8000", host: "localhost", referrer: "http://elocalhost/"
```

可以看到后端链接被拒绝，nginx页面返回的是502。此种情况，大多为uwsgi的配置问题。可从以下几点排查：

- 地址和端口号配置`socket`, 注意127.0.0.1和0.0.0.0的区别。
- `sockect`和`http`都可以指定地址和端口，当使用nginx代理时，注意配置，

```
sockect --- >  uwsgi_pass 
http ---> proxy_pass 
```

**3、uWSGI的安装位置**

在部署项目时，经常会用到`virtualenv`来生产虚拟环境来隔离系统的python环境，此时我们需要注意，安装uWSGI和运行django的python环境需要是同一个。


**4、启动后uwsgi报错：-- unavailable modifier requested: 0 --**

造成此错误的原因是uWSGI安装的python和项目使用的不是一个，重新安装uWSGI即可。使用项目相同的python编译安装，或直接使用项目使用python的包管理工具安装，如pip、pipenv。



>TODO待补充

欢迎大家在下方留言，提交自己遇到的问题，我们来共同交流探讨~ 