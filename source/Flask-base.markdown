---
layout : post
title : Flask 目录结构分析
category : Flask
date : 2018-06-04
tags : [Flask, python]
---
 
到目前为止，Flask 最新版本为`1.0.3`，我们来以此版本做分析，以便可以快速回忆各组件关系。

基本使用，可参阅[官方文档](http://flask.pocoo.org/docs/1.0/)，已非常详尽。

我们知道Flask，是一个`微`框架，只所以叫`微`是因为它没有像Django那样把所有的事情都帮你处理了。它只提供给我们web开发很核心的部分，其他的像数据库处理、模板引擎的选择等都交给了外部的插件处理。这也是Flask的一大特点，插件化。我们可以很灵活的组织我们的项目框架。但有选择，就有问题，这是一柄双刃剑。随着Flask插件生态的繁荣，它已经可以满足大多数的项目需求。甚至github的收藏数已超过Django,稳居python web开发框架之首。一切事物都是相对的，框架亦是如此，没有优劣，只有合适与否。

那么Flask的插件是如何运作的，一个基本的Flask开发框架都需要什么模块呢？让我们带着这些问题，展开今天的分析。
<!-- more -->
### 一个最小的Flask应用

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

分析：
- 1、首先初始化了Flask引用的实例`app`，这个实例可以提供给`wsgi`协议的web服务器来运行。也可通过如上的`run()`函数自己运行，不过这个只限开发，性能非常低下。
- 2、接下来，在这个`app`上注册了路由，和处理函数。我们大部分的业务逻辑应该在这个处理函数中。
- 3、最后，直接返回数据，并没有涉及模板和数据库。

### 完整项目分析

以 `cookiecutter` 模板为例：[flask_boilerplate](https://github.com/pylixm/flask_boilerplate)

项目目录结构如下：

```
$ tree
.
├── LICENSE
├── Procfile  
├── README.rst
├── assets   # 静态文件，提供给webpack打包使用
│   ├── css 
│   │   └── style.css
│   ├── img
│   └── js
│       ├── main.js
│       ├── plugins.js
│       └── script.js
├── autoapp.py  # flask app 启动入口
├── flask_boilerplate  # flask 代码目录 
│   ├── __init__.py   
│   ├── app.py   # flask app 创建代码
│   ├── commands.py   # flask 命令扩展代码
│   ├── compat.py   # python 2和3 的兼容代码
│   ├── database.py   # 数据库 model 代码，可根据复杂程度，分拆多个模块文件
│   ├── extensions.py   # 扩展统一实例化，方便控制前后顺序，防止循环引用
│   ├── public   # 蓝图
│   │   ├── __init__.py 
│   │   ├── forms.py  
│   │   └── views.py
│   ├── settings.py   # 项目整体配置
│   ├── static   # 静态文件，Flask 默认目录
│   │   └── build
│   ├── templates   # 模板文件，flask 默认目录
│   │   ├── 401.html
│   │   ├── 404.html
│   │   ├── 500.html
│   │   ├── footer.html
│   │   ├── layout.html
│   │   ├── nav.html
│   │   ├── public
│   │   │   ├── about.html
│   │   │   ├── home.html
│   │   │   └── register.html
│   │   └── users
│   │       └── members.html
│   ├── user    # 蓝图
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   └── views.py
│   └── utils.py  工具包
├── package.json   # npm 配置文件
├── requirements  # python 模块列表
│   ├── dev.txt
│   └── prod.txt
├── requirements.txt
├── setup.cfg
├── tests
└── webpack.config.js  # webpack配置文件
```

我们先忽略其他最外层的配置文件，从入口`autoapp.py`分析 ：

```python
# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from flask_boilerplate.app import create_app
from flask_boilerplate.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)

```

分析：
- 1、实例化了Flask 应用，供外部启动使用。
- 2、使用全局的配置文件`CONFIG`,并根据是否调式调用不同的配置项。

我们继续，到`app` 文件：

```python
# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from flask_boilerplate import commands, public, user
from flask_boilerplate.extensions import bcrypt, cache, csrf_protect, db, \
    debug_toolbar, login_manager, migrate, webpack
from flask_boilerplate.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app

.....

```
分析：
- `create_app` 函数，在实例化app后，往app上注册了一些基本的扩展和蓝图，以及错误处理和命令上下文等。充分体现了插件的思想。

那么各模块便体现在 `register_extensions` 这个函数中：

```python
def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    webpack.init_app(app)
    return None
```
可以根据命名开出，其中许多必备的扩展插件，如数据库插件。

除了从功能上来进行扩展外，我们的业务逻辑也可通过`蓝图`实现插件化, 如下：

```python
def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None
```

我们的业务逻辑便在这些蓝图中实现。这样我们整个Flask框架整个开发架构便清晰了：

- 通过扩展来扩展框架功能
- 通过蓝图来模块化我们的业务逻辑



