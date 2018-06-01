---
layout : post
title : django 相关命令总结
category : django
date : 2016-01-29 18:00:00
tags : [django,]
---



## django 常用命令 

创建一个web站点：

    django-admin.py startproject mysite

创建apps：

    python manage.py startapp blog
    
数据库模板检测：

    python manage.py validate

生成数据库表创建语句：

    python manage.py sqlall books（app名字）
    
创建数据库表：

    python manage.py syncdb
    注意：Django 1.7.1及以上的版本需要用以下命令
    python manage.py makemigrations # 检查
    python manage.py migrate #执行
    
    migrate: 用于执行迁移动作，具有syncdb的功能
    makemigrations: 基于当前的model创建新的迁移策略文件
    sqlmigrate: 显示迁移的SQL语句，具有sqlall的功能

清空数据库（慎用）:

    python manage.py flush
    
创建超级管理员:

    python manage.py createsuperuser

收集静态文件：

    python manage.py collectstatic

## django celery 常用命令

默认 queue

    python manage.py celery worker -Q celery

高优先级 queue. 10个 workers

    python manage.py celery worker -Q high -c 10

低优先级 queue. 2个 workers
    
    python manage.py celery worker -Q low -c 2

Beat 进程

    python manage.py celery beat



#### 参考

* [http://www.ziqiangxuetang.com/django/django-basic.html](http://www.ziqiangxuetang.com/django/django-basic.html)