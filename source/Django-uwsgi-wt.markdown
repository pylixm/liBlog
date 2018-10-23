---
layout : post
title : Django uwsgi 启动问题 unavailable modifier requested 0
category : QA
date : 2016-01-18 19:55:00
tags : [QA, django, uwsgi]
---



### Q & A：

    mapped 1263744 bytes (1234 KB) for 16 cores
    *** Operational MODE: preforking+threaded ***
    *** no app loaded. going in full dynamic mode ***
    *** uWSGI is running in multiple interpreter mode ***
    spawned uWSGI master process (pid: 2343)
    spawned uWSGI worker 1 (pid: 2345, cores: 2)
    spawned uWSGI worker 2 (pid: 2346, cores: 2)
    spawned uWSGI worker 3 (pid: 2348, cores: 2)
    spawned uWSGI worker 4 (pid: 2350, cores: 2)
    spawned uWSGI worker 5 (pid: 2352, cores: 2)
    spawned uWSGI worker 6 (pid: 2354, cores: 2)
    spawned uWSGI worker 7 (pid: 2356, cores: 2)
    spawned uWSGI worker 8 (pid: 2358, cores: 2)
    -- unavailable modifier requested: 0 --
<!-- more -->
### 引起原因

uwsgi 启动时，找不到python引起。使用 yum 等工具安装造成。

### 解决方案：

方法一：

安装uwsgi-plugin-python，并且在uwsgi的配置文件中指定“plugins = python”。

方法二：

直接编译安装uwsgi

方法三：

使用pip 安装，因为pip是依赖python的，安装时会绑定其使用的python。

---

#### 参考：

- [http://www.dannysite.com/blog/197/](http://www.dannysite.com/blog/197/)

- [http://stackoverflow.com/questions/10748108/nginx-uwsgi-unavailable-modifier-requested-0](http://stackoverflow.com/questions/10748108/nginx-uwsgi-unavailable-modifier-requested-0)

- [http://serverfault.com/questions/426039/nginx-uwsgi-unavailable-modifier-requested-0](http://serverfault.com/questions/426039/nginx-uwsgi-unavailable-modifier-requested-0)



