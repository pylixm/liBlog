---
layout : post
title : Django学习笔记- Class View
category : django
date : 2016-03-24
tags : [django, Classview]
---


**提示**：文章概念性语句比较多，建议先看 Classview 的[官方文档](https://docs.djangoproject.com/en/1.9/topics/class-based-views/)或[1.8 中文翻译文档](http://python.usyiyi.cn/django_182/topics/class-based-views/index.html)。

之前使用 `django` 开发都是使用 func-view ，对Classview一直是向往的。

最近有些时间，看下Classview的用法，记录下，备查。


### 0x01 使用目的及优势

- HTTP 方法（GET、POST 等）可以有各自的方法，而不用通过条件分支来解决。

- 面向对象的技术例如Mixin（多继承）可以将代码分解成可重用的组件。

- 更好的利用 `通用视图`。(基于函数的通用视图难易扩展，基于类的可以通过 Mixin 来扩展，更加灵活)

### 0x02 Classview 原理

Django 的URL 解析器将请求和关联的参数发送给一个可调用的函数而不是一个类，所以基于类的视图有一个as_view() 类方法用来作为类的可调用入口。

该as_view 入口点创建类的一个实例并调用dispatch() 方法。dispatch 查看请求是GET 还是POST 等等，并将请求转发给相应的方法，

如果该方法没有定义则引发HttpResponseNotAllowed。

### 0x03 用法筛记 

#### Classview 中装饰器的用法

- 在urlconf 中直接装饰 `as_view()` 函数。

```python

from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

from .views import VoteView

urlpatterns = [
    url(r'^about/', login_required(TemplateView.as_view(template_name="secret.html"))),
    url(r'^vote/', permission_required('polls.can_vote')(VoteView.as_view())),
]

```

- 使用 `method_decorator` 转化后直接装饰到 class 的方法上 

```python

    from django.contrib.auth.decorators import login_required
    from django.utils.decorators import method_decorator
    from django.views.generic import TemplateView

    class ProtectedView(TemplateView):
    
        template_name = 'secret.html'

        @method_decorator(login_required)
        def dispatch(self, *args, **kwargs):
            return super(ProtectedView, self).dispatch(*args, **kwargs)
            
```
  
### 0x04 扩展通用视图的方法

- 在url 中直接传递参数，覆盖类属性，到达扩展的作用。

- 编写其子类，覆盖其方法。


### 0x05 通用视图基本用法要点总结

- context_object_name 属性指定要使用的上下文变量，默认的是 object_list 

- model参数指定视图在哪个数据库模型之上进行操作

- template 指定视图模板 

- 可以使用 get_context_data 指定额外的上下文变量 

- 可以使用 get_query 指定经过逻辑过滤的处理对象（queryset 同 model ）

- form_class 指定操作的Form

 
### 0x06 常用视图解析

#### 1、通用模板视图 `TemplateView`
 
 ![][1]

`ContextMixin` 提供上线文context 
`View` 提供 as_view 函数
`TemplateResponseMixin` 返回TemplateResponse 对象，template 使用的是类属性 tempalte_name。

#### 2、通用列表视图 `ListView`和通用详情页视图 `DetailView`

![][2]


![][3]

（原图片出处[博客](http://blog.csdn.net/hackerain/article/details/40919789)中描述，直接搬过来了）

在这两个类图中，最关键的组件就是MultiObjectMixin和SingleObjectMixin这两个类了，他们实现的功能是从数据库中读取数据，

并且构建要传入template的context。每个类都有一些属性和方法可以覆盖，实现自定制，比如可以覆盖context_object_name变量，

用来指定传入template的context的对象的变量名；可以覆盖get_context_data()方法，用来将其他的变量放到context中；

为queryset赋值，就可以自己指定这个View操作的对象(列表)；或者是直接重写get_queryset()/get_object()方法，简单暴力。

注意，这两个类，也是继承自TemplateResponseMixin，也就是说它们也是直接返回的TemplateResponse对象。





### 0x07 其他知识点

- 对于每个请求都会实例化类的一个实例，但是as_view() 入口点设置的类属性只在URL 第一次导入时配置。

- 只能继承一个通用视图 —— 也就是说，只能有一个父类继承View，其它的父类必须是Mixin

- 你的视图扩展应该仅仅使用那些来自于同一组通用基类的view或者mixins


#### 参考

[http://blog.csdn.net/hackerain/article/details/40919789](http://blog.csdn.net/hackerain/article/details/40919789) 

[http://python.usyiyi.cn/django/topics/class-based-views/index.html](http://python.usyiyi.cn/django/topics/class-based-views/index.html)

[http://blog.csdn.net/hackerain/article/details/40919789](http://blog.csdn.net/hackerain/article/details/40919789)


[1]:/static/imgs/TemplateView.png
[2]:/static/imgs/ListView.png
[3]:/static/imgs/DetailView.png
