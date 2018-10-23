---
layout : post
title : Django 最佳实践-读书笔记 - 第一章 代码规范 
category : django
date : 2016-05-22
tags : [django]
---

[其他章节索引页](2016-05-22-Best.Practices.for.Django.1.8.3rd-Index.html)

# 核心理念

- Keep It Simple, Stupid
- Fat Models, Utility Modules, Thin Views, Stupid Templates
- Start With Django by Default
- Be Familiar with Django's Design Philosophies
- The Twelve-Factor App
<!-- more -->
# 第一章 代码规范

## 常规：

- 变量名，避免缩写
- 写出你的函数参数名
- 编写类和方法的 doc string 
- 评审你的代码
- 提取重构重复使用的代码
- 保持函数方法简短。一个好的原则，可以不滚动，看全这个函数方法。

## PEP 8 的规范

注：
 - 不要为了适应PEP8，改变已有项目的编码约定。

 - 在一个开源项目中，一行代码限定在 79 个字符长度；在自己私有的项目中，这个限定可放宽到99个字符。

## 导入模块：


### 模块顺序：

- 标准库
- django 核心库
- 第三方 app 
- 自定义的 app

example:

```python
# Stdlib imports
from __future__ import absolute_import
from math import sqrt
from os.path import abspath
# Core Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Third-party app imports
from django_extensions.db.models import TimeStampedModel
# Imports from your apps
from splits.models import BananaSplit
```

### 相对导入

```
# cones/views.py
from __future__ import absolute_import
from django.views.generic import CreateView
# Relative imports of the 'cones' package
from .models import WaffleCone
from .forms import WaffleConeForm
from core.views import FoodMixin
class WaffleConeCreateView(FoodMixin, CreateView):
model = WaffleCone
form_class = WaffleConeForm
```

### 导入模块时，避免使用 * 


## django 中的代码规范

- url 名称使用下划线，不要使用横线
- 在模板 block中，名称使用下划线，不要使用横线

