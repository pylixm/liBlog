---
layout : post
title : Django 最佳实践-读书笔记 - 第五章 Settings 和 Requirements
category : django
date : 2016-05-22
tags : [django]
---

[其他章节索引页](2016-05-22-Best.Practices.for.Django.1.8.3rd-Index.html)

# 第五章 Settings 和 Requirements

## 避免本地未受控的 settings 文件

- 代码维护困难
- 多人开发时，勿提交local settings 文件，造成配置混乱。

## 使用多分配置文件

```python
settings/
    __init__.py
    base.py
    local.py
    staging.py
    test.py
    production.py
```

### 使用：

方法一：

    python manage.py shell --settings=twoscoops.settings.local
    python manage.py runserver --settings=twoscoops.settings.local

方法二：

通过设置`DJANGO_SETTINGS_MODULE` 和 `PYTHONPATH`环境变量来代替 `--settings` 参数

方法三：

设置 virtualenv 的postactivate 脚本，在启动环境时，配置`DJANGO_SETTINGS_MODULE` 和 `PYTHONPATH`环境变量。

## 多开发配置文件 

多人开发时，可提交自己的开发配置文件。

```python
settings/
    __init__.py
    base.py
    dev_audreyr.py
    dev_pydanny.py
    local.py
```

## 将秘钥等安全性高的变量放到环境变量中

注意：

Apache 有自己的环境变量系统，需要注意区分。

### 设置

```bash
$ export SOME_SECRET_KEY=1c3-cr3am-15-yummy
$ export AUDREY_FREEZER_KEY=y34h-r1ght-d0nt-t0uch-my-1c3-cr34m
```

### 获取

```python 
>>> import os
>>> os.environ["SOME_SECRET_KEY"]
"1c3-cr3am-15-yummy"

```

配置文件使用：

```
# Top of settings/production.py
import os
SOME_SECRET_KEY = os.environ["SOME_SECRET_KEY"]
```

## 在settings配置文件中不要使用绝对路径

## Requirements 管理思路和 settings一致 

