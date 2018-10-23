---
layout : post
title : 译-在django中使用celery实现异步任务
category : django
date : 2015-12-03 16:00:00
tags : [django, celery, 翻译]
---



### 在django中使用celery

在使用celery时，你需要定义一个celery的实例（叫做 app ）。如果你有一个现成的django项目，如下：

```python
- proj/
  - proj/__init__.py
  - proj/settings.py
  - proj/urls.py
- manage.py
```
<!-- more -->
建议如下方式创建celery实例。

创建 proj/proj/celery.py 文件，如下：

``proj/proj/celery.py``

```python
from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

from django.conf import settings  # noqa

app = Celery('proj')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
```

接下来，你需要把这个app放到``proj/proj/__init__.py``模块中，确保django启动的时候这个app能够被加载。

从而提供给``@shared_task``(稍后讲到)注解使用。

``proj/proj/__init__.py``

```python
from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app  # noqa
```

注意，这个项目实例的布局，适合于大型项目。对于简单的小项目来说，你可以用一个模块来同时定义celery实例和任务。

参考celery [入门教程](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#tut-celery)教程。

让我们逐个分析下第一个模块都做了什么。

首先，我们导入``future`` 模块，让我们的``celery.py`` 不会与其他类库产生冲突。

    from __future__ import absolute_import
    
接下来，我们为celery 设置类默认的django项目 ``DJANGO_SETTINGS_MODULE ``。 

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
    
这个设置让celery程序知道我们的django项目配置在哪。这句必须放在celery每次被实例化之前。

接下来，实例化 celery 。

    app = Celery('proj')
    
在django项目中，你只需要一个celery实例就可以了。

我们可以把celery的配置放到django的settings配置文件中，如下：

    app.config_from_object('django.conf:settings')
    
此处的参数你可以传递对象，但是建议字符串，这样使用windows 或execv 的时候，无需序列化对象。

接下来，将所有可以重复操作的任务tasks.py 放到一个django的app中，celery使用如下的机制来发现此模块。

    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

tasks.py 的放至如下：

    - app1/
        - app1/tasks.py
        - app1/models.py
    - app2/
        - app2/tasks.py
        - app2/models.py
        
这样，您就不必在各个模块手动添加到CELERY_IMPORTS参数。lambda 函数会使app在调用的时候能够被自动的发现，并且使你输入的模块不会影响Django的设置对象。
        
最后，debug_task 例子是绑定了自己的request请求信息的一个任务函数。

Finally, the debug_task example is a task that dumps its own request information. 

This is using the new bind=True task option introduced in Celery 3.1 to easily refer to the current task instance.


### Using the @shared_task decorator

你的task任务写在了django的app中，这个app可能不依赖与django项目本身。所以你不能讲celery的实例一如此app中。

该@shared_task装饰可以让你创建任务，而无需任何具体的celery实例：

注：此时需要把 django 的app 添加到 settings的app列表（INSTALLED_APPS）中。

demoapp/tasks.py:

```python
from __future__ import absolute_import

from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
```

### Using the Django ORM/Cache as a result backend.

如果你想讲celery的返回结果使用django的ORM（或SQLAlchemy）存到数据库中，你需要安装 django-celery 模块库。

django-celery 模块库结果默认使用django的ORM 和 Cache 框架。

使用步骤如下：

1、安装 django-celery 库：

    $ pip install django-celery
    
2、Add djcelery to INSTALLED_APPS.

3、创建celery的数据表

    If you are using south for schema migrations, you’ll want to:
    
    $ python manage.py migrate djcelery
    For those who are not using south, a normal syncdb will work:
    
    $ python manage.py syncdb

    >=django1.7 
    可直接使用django自带的数据库同步命令：
    $ python manage.py makemigrations
    $ python manage.py migrate

4、配置celery。

    # For the database backend you must use:
    app.conf.update(
        CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    )
    # For the cache backend you can use:
    app.conf.update(
        CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',
    )
    # 此处配置用来存储任务执行结果。
    
除了这种方式外，你可以把 CELERY_RESULT_BACKEND 放到你的django的settings配置文件中。


### Starting the worker process

在生产环境中，你将希望在后台运行worker - 请参阅 [ Running the worker as a daemon](http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html#daemonizing) - 

但对于测试和开发它能够通过使用 celery 启动工作实例的管理命令非常有用，

就像你使用Django的runserver：

    celery -A proj worker -l info
    
获取完整的celery命令列表，请使用：

    celery help 
    
    
### 2015年12月10日 update：
    
按照此教程，启动celery后，报错误如下：

    [2016-05-29 01:19:24,751: ERROR/MainProcess] consumer: Cannot connect to amqp://guest:**@127.0.0.1:5672//: [Errno 111] Connection refused.
    Trying again in 2.00 seconds...

原因是，celery 需要一个 `broker` 来发送和接收消息，支持：rabbitmq、redis、数据库等作为这个broker。上边的配置中没有设置这个borker，

celery 默认使用 rabbitmq来作为broker。所以，报错链接不上rabbitmq。

解决办法：

1、按装rabbitmq 显式的指定 broker为你配置的rabbitmq。

    CELERY_BROKER_URL = 'amqp://guest:guest@localhost//' 

2、使用django数据库作为 broker：

    # 增加配置
    BROKER_URL = 'django://'
    # 增加app实例配置
    INSTALLED_APPS = ('kombu.transport.django', )
    
broker 官方建议使用 rabbitmq 或 redis ，其他的broker 仅为开发测试，性能不稳定。

官网详细介绍：http://docs.jinkan.org/docs/celery/getting-started/brokers/index.html


### 2016年5月29日 更新：

在搭建django + celery 使用总结：

1、使用 ` app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)`这个配置，让celery 自动发现django app 下定义的task 时， django app下的task 文件名 必须为 `tasks.py`。

2、celery 3.1 后，和django的结合无需再依靠django-celery。 可按以上方式搭建。具体官方地址 [这里](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)

3、todo 后续补充


### 各种功能搭建实例源码

[源码](https://github.com/pylixm/celery-examples/tree/master)

---

**ps: 个人英文水平有限，还请各位批评指正。**

### 参考：

[http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)
