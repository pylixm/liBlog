---
layout : post
title : Django 最佳实践-读书笔记 - 第十三章 模板最佳实践
category : django
date : 2016-07-02 
tags : [django]
---

[其他章节索引页](2016-05-22-Best.Practices.for.Django.1.8.3rd-Index.html)

笔记以要点形式展开，如有疑问欢迎留言！

# 第十三章 模板最佳实践

django 的模板的局限性，限制了我们将复杂的逻辑放在了 `python` 端，这何尝不是一件好事。

从 django 1.8 开始，django 原生支持了 jinjia2 模板。

## 尽量保持大多数的模板文件在目录 `templates/` 下

```
templates/
    base.html
    ... (other sitewide templates in here)
    freezers/ ("freezers" app templates in here)
```

将模板放在 app 下 templates 是没有必要的，因为当app 作为可拔插的包拿来使用的时候，它的模板会被重新设计。
索性将所有app 模板放到templates 下，好维护些。


## 模板的架构模式

### 2 层嵌套模式 

2 层嵌套模式适合于全站统一布局的情况。

```python
templates/
base.html
dashboard.html # extends base.html
    profiles/
        profile_detail.html # extends base.html
```

### 3 层嵌套模式

3 层嵌套适合于每个app 需要自己的布局的情况。

```python
templates/
base.html
dashboard.html # extends base.html
    profiles/
        base_profiles.html # extends base.html
        profile_detail.html # extends base_profiles.html
        profile_form.html # extends base_profiles.html
```

### 扁平比嵌套好 

## 在模板中限制逻辑处理

### 当在模板中遍历结果集时注意的问题：

- 不要在模板中遍历巨大的结果集
- 检索的对象多大，是不是所有的对象在模板中都需要
- 将逻辑处理移出循环，不要重复处理，拖慢循环处理。

### 在使用 cache 之前，尝试优化，重构你的代码

### 保持模板简单，尽量少使用 js 或 filter 来处理数据，这样会拖慢你的页面

### 不要在模板中的结果集中遍历查询对象

Bad Example :
```html
<h2>Greenfelds Who Want Ice Cream</h2>
<ul>
{% for voucher in voucher_list %}
    {# Don't do this: conditional filtering in templates #}
    {% if "greenfeld" in voucher.name.lower %}
        <li>{{ voucher.name }}</li>
    {% endif %}
{% endfor %}
</ul>
<h2>Roys Who Want Ice Cream</h2>
<ul>
{% for voucher in voucher_list %}
    {# Don't do this: conditional filtering in templates #}
    {% if "roy" in voucher.name.lower %}
        <li>{{ voucher.name }}</li>
    {% endif %}
{% endfor %}
</ul>


```

Right Exemple:

```python
# vouchers/views.py
from django.views.generic import TemplateView
from .models import Voucher


class GreenfeldRoyView(TemplateView):
    template_name = "vouchers/views_conditional.html"
    
    def get_context_data(self, **kwargs):
        context = super(GreenfeldRoyView, self).get_context_data(**kwargs)
        context["greenfelds"] = \
        Voucher.objects.filter(name__icontains="greenfeld")
        context["roys"] = Voucher.objects.filter(name__icontains="roy")
        return context
```

```html
<h2>Greenfelds Who Want Ice Cream</h2>
<ul>
{% for voucher in greenfelds %}
    <li>{{ voucher.name }}</li>
{% endfor %}
</ul>
<h2>Roys Who Want Ice Cream</h2>
<ul>
{% for voucher in roys %}
    <li>{{ voucher.name }}</li>
{% endfor %}
```

### 不要在模板中隐含复杂的查询 

Bad exemple:
```html
{# list generated via User.object.all() #}
<h1>Ice Cream Fans and their favorite flavors.</h1>
<ul>
{% for user in user_list %}
    <li>
    {{ user.name }}:
    {# DON'T DO THIS: Generated implicit query per user #}
    {{ user.flavor.title }}
    {# DON'T DO THIS: Second implicit query per user!!! #}
    {{ user.flavor.scoops_remaining }}
    </li>
{% endfor %}
</ul>
```

Right Exemple:

```html
{# 生成列表的时使用： User.object.all().select_related("flavors") #}

<h1>Ice Cream Fans and their favorite flavors.</h1>
<ul>
{% for user in user_list %}
    <li>
    {{ user.name }}:
    {{ user.flavor.title }}
    {{ user.flavor.scoops_remaining }}
    </li>
{% endfor %}
</ul>
```

### 模板尽量避免加载导致cpu使用过高的对象

例如图片的加载，尽量使用模板外部的工具。

详见：13.3.4 Gotcha 4: Hidden CPU Load in Templates

### 不要在模板中调用 rest api 

当我们在模板中调用 rest api 时，注意：

- 在js请求数据，加载时，你需要分散你客户的注意力。
- python 处理缓慢的进程方式更多：消息队列，多线程，多进程等。

## 使用缩进来使你的模板更加易读

## block.super 的使用,来更好的使用继承特性

```html
{# simple base.html #}
{% load staticfiles %}
<html>
<head>
<title>
    {% block title %}Two Scoops of Django{% endblock title %}
</title>
    {% block stylesheets %}
        <link rel="stylesheet" type="text/css"
        href="{% static "css/project.css" %}">
    {% endblock stylesheets %}
</head>
<body>
    <div class="content">
        {% block content %}
            <h1>Two Scoops</h1>
        {% endblock content %}
    </div>
</body>
</html>
```

```html
{% extends "base.html" %}
{% load staticfiles %}
{% block title %}About Audrey and Daniel{% endblock title %}
{% block stylesheets %}
    {{ block.super }}
    <link rel="stylesheet" type="text/css"
    href="{% static "css/about.css" %}">
{% endblock stylesheets %}
{% block content %}
    {{ block.super }}
    <h2>About Audrey and Daniel</h2>
    <p>They enjoy eating ice cream</p>
{% endblock content %}
```

## 一些有用的技巧

### 样式的控制和 python的要松耦合

### 一些通用的约定

- 使用下划线来命名模板名称，block 名称。

- block 的名字要清晰，如{% block javascript %}`

- 在 block 结束时，也要写上名称，如 `{% endblock javascript %}`.

### 使用具体的 model 对象名来命名模板对象列表

```html
{# toppings/topping_list.html #}
{# Using implicit names #}
<ol>
    {% for object in object_list %}
        <li>{{ object }} </li>
    {% endfor %}
</ol>

{# Using explicit names #}
<ol>
    {% for topping in topping_list %}
        <li>{{ topping }} </li>
    {% endfor %}
</ol>

```

### 使用 url 名字来代替硬编码的url 

```html
Bad exemple:
<a href="/flavors/">

Right exemple:
<a href="{% url 'flavors_list' %}">
```

### debug 的时候可以开启，页面详细错误

```python
# settings/local.py
TEMPLATES = [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS':
        'string_if_invalid': 'INVALID EXPRESSION: %s'
    },
]
```

## 错误模板的设置

在生产环境中，一定要设置错误页面，但不要过使页面复杂。


# 第十四章 模板的 tags 和 filters 

## filter 什么时候使用

- 格式化模板中数据
- rest api 中数据的格式化

## 自定义 tags 

尽量书写少的tags ：

- tags 比较难调试
- 使代码不容易重用
- 性能消耗比较大 

## 命名 tags 类库 

<app name> tags.py

## 在 template 页面中加载 tags 

```html
{% extends "base.html" %}
{% load flavors_tags %}

# Don't use this code!
# It's an evil anti-pattern!
from django import template
template.add_to_builtins(
    "flavors.templatetags.flavors_tags"
)
```

# 第十五章 Django 模板（DTL） 和 jinja2

## 不同之处 

![](/static/imgs/df.png)

## 我们应该如何选择

### DTL 的优点

- django 的所有官方文档使用 DTL，便于理解。
- django + DTL 的组合更成熟。
- 大多数的django 三方包使用的是 DTL。
- 转化 DTL到jinja2需要大量的工作。

### jinjia2 的优点

- 在django中可以被单独使用。
- jinja2 的语法更接近 python的语法。
- jinja2 更明确，例如函数的调用带有括号。
- jinja2 有更少的限制，例如可以给一个filter传递无限个参数。而DTL 只能传一个。
- jinja2 渲染更快。

### 如何选择

- 新手建议使用 DTL
- 页面简单的使用 DTL ，复杂的使用 jinja2 
- 一个项目中，我们可以2个都使用。一个作为主要的模板，另一个为辅。

## jinja2 部分使用举例

### CSRF 

```html
<div style="display:none">
<input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
</div>
```

### jinja2 无法使用 自定义 tags的 

### jinja2 中使用 django-style 的  filter

```python
# core/jinja2.py
from __future__ import absolute_import # Python 2 only
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.template import defaultfilters

from jinja2 import Environment
def environment(**options):
    env = Environment(**options)
    env.globals.update({
    'static': staticfiles_storage.url,
    'url': reverse,
    'dj': defaultfilters
    })
    return env

```  

```html
<table><tbody>
{% for purchase in purchase_list %}
    <tr>
    <a href="{{ url("purchase:detail", pk=purchase.pk) }}">
        {{ purchase.title }}
    </a>
    </tr>
    <tr>{{ dj.date(purchase.created, "SHORT_DATE_FORMAT") }}</tr>
    <tr>{{ dj.floatformat(purchase.amount, 2) }}</tr>
{% endfor %}
</tbody></table>
```


### 上下文 context 不能在 jinja2 中使用

我们可以自定义中间件

```python
# advertisements/middleware.py
import random
from advertisements.models import Advertisement as Ad

def AdvertisementMiddleware(object):
    def process_request(request):
        count = Advertisement.objects.filter(subject='ice-cream').count()
        ads = Advertisement.objects.filter(subject='ice-cream')
        # If necessary, add a context variable to the request object.
        if not hasattr(request, 'context'):
        request.context = {}
        # Don't overwrite the context, instead we build on it.
        request.context.update({'ad': ads[random.randrange(0, count)]})

<!-- base.html -->
{% set ctx = request.context %}
...
<div class="ice-cream-advertisement">
    <a href="{{ ctx.ad.url }}">
        <img src="ctx.ad.image.url" />
    </a>
</div>
``` 

