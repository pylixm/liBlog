---
layout : post
title : Django restfull framework 使用笔记 -- 踩坑记录
category : django
date : 2016-11-30 
tags : [django, restfull]
---

在使用django restfull 时，遇到的几个不好发现的问题，记录如下备查。

## 一、 缓存问题 

在系统与外部系统以http接口的方式做交互时，发现我们使用drf（django restfreamwork）框架实现的接口数据多次调用获取到的数据值不一致。

首先，我们想到的是缓存，但是经过排查，系统中并没有使用外部的缓存。那么既有可能是drf 内部有缓存机制，于是去官方文档查阅。最后找到了这样的描述：

```python
get_queryset(self)

Returns the queryset that should be used for list views, and that should be used as the base for lookups in detail views. Defaults to returning the queryset specified by the queryset attribute.

This method should always be used rather than accessing self.queryset directly, as self.queryset gets evaluated only once, and those results are cached for all subsequent requests.
```
`get_queryset` 这个函数会缓存数据列表，当数据列表有更新时，再次查询数据便造成了数据的不一致。

重写此方便可以根据request 来给 view 提供不同的queryset，但是翻遍了官方文档，查看了源码仍然没有找到一个既可以重写此方法又可以不缓存的方案，此方法还是慎用。

总结，views 中 get_queryset 可以根据request来个性化的定制queryset，但会缓存数据，可能造成数据不一致风险。

大批量数据且改动比较少的数据，可使用此方法。改动比较频繁的数据列表，误用此方法。


## 二、自带的seralizer继承 HyperlinkedModelSerializer时钻取问题

当序列化类为HyperlinkedModelSerializer类型时，注意钻取的深度。当设计到django自带的model时,比如User表的权限model，需要注意，会报：

```python
Could not resolve URL for hyperlinked relationship using view name "permission-detail". 
You may have failed to include the related model in your API, or incorrectly configured the `lookup_field` attribute on this field.
```

此处设计到用户权限表，实际生产中此表肯定是不能暴露给接口外部的。所以，此处没有再进一步深究。想来，重写或显示的写出model，应该是有办法解决的。

总结，序列化类编写时，注意类型的合理应用。使用链接钻取类时，注意深度，避免不必要的错误。


# todo 待续

---

#### 参考： 

- [http://www.django-rest-framework.org/](http://www.django-rest-framework.org/)