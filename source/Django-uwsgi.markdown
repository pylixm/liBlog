---
layout : post
title : Django uwsgi 启动问题 ImportError No module named os
category : QA
date : 2015-11-23 16:00:00
tags : [QA, django]
---



### Q & A：

今天在搭建测试环境时遇到问题，如下
	
	*** WARNING: you are running uWSGI without its master process manager ***
	your processes number limit is 65535
	your memory page size is 4096 bytes
	detected max file descriptor number: 65536
	lock engine: pthread robust mutexes
	thunder lock: disabled (you can enable it with --thunder-lock)
	uwsgi socket 0 bound to TCP address 0.0.0.0:8002 fd 3
	Python version: 2.6.6 (r266:84292, Jan 22 2014, 09:42:36)  [GCC 4.4.7 20120313 (Red Hat 4.4.7-4)]
	Set PythonHome to /usr/local/cms_env
	'import site' failed; use -v for traceback
	Python main interpreter initialized at 0x2841d20
	python threads support enabled
	your server socket listen backlog is limited to 100 connections
	your mercy for graceful operations on workers is 60 seconds
	mapped 1123328 bytes (1097 KB) for 16 cores
	*** Operational MODE: preforking+threaded ***
	Traceback (most recent call last):
	  File "./cms/wsgi.py", line 16, in <module>
	    import os
	ImportError: No module named os
	unable to load app 0 (mountpoint='') (callable not found or import error)
	*** no app loaded. going in full dynamic mode ***
	*** uWSGI is running in multiple interpreter mode ***
	spawned uWSGI worker 1 (pid: 16882, cores: 2)
	spawned uWSGI worker 2 (pid: 16886, cores: 2)
	spawned uWSGI worker 3 (pid: 16887, cores: 2)
	spawned uWSGI worker 4 (pid: 16888, cores: 2)
	spawned uWSGI worker 5 (pid: 16891, cores: 2)

<!-- more -->
导致uwsgi 启动失败。仔细查看以上日志，python 的版本为2.6，自己明明已经升级为2.7了。在命令行打印python版本也是2.7，如下：

	Python 2.7.10 (default, Nov 20 2015, 19:10:34) 
	[GCC 4.4.7 20120313 (Red Hat 4.4.7-11)] on linux2
	Type "help", "copyright", "credits" or "license" for more information.
	>>> 

如何应该是虚拟环境的路径问题，导致python的路径出错。查看文档，虚拟环境的路径 使用 home/virtualenv（http://uwsgi-docs.readthedocs.org/en/latest/Python.html?highlight=virtualenv） 来定义。我的配置文件如下：

	
	[uwsgi]
	socket = 0.0.0.0:80
	chdir = /usr/local/mysite/
	module = mysite.wsgi:application
	virtualenv = /usr/local/mysite_env
	processes = 8
	threads = 2
	daemonize = /usr/local/mysite/mysite.log
	pid-file = /usr/local/mysite/mysite_uwsgi.pid
	vacuum = True
	buffer-size = 32768

仔细核对应该没有什么问题。


### 解决方案：

经过查询，果然有人遇到和我一样的错误。参考其，解决办法，果然得到了解决。

大致原因如下：

uwsgi的版本是在python2.6下编译安装的，所以调用时，它默认使用了2.6。 重新卸载uwsgi，在python2.7下编译安装，即可解决此类问题。

另： 在 virtualenv 下安装的uwsgi 直接使用uwsgi或 绝对路径即可，注意与 /usr/bin/uwsgi /usr/local/bin/uwsgi 两路径下的版本区别。


---

#### 参考：

[http://stackoverflow.com/questions/25757552/importerror-no-module-named-os-uwsgi-django-linux](http://stackoverflow.com/questions/25757552/importerror-no-module-named-os-uwsgi-django-linux)



