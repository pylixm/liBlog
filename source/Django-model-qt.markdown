---
layout : post
title : Django学习笔记- 自定义管理器（objects）后遇到的问题
category : django
date : 2016-04-20
tags : [django, model]
---

### 管理器自定义简介

django model 的管理器 objects 允许我们自定义，这大大的扩展了model的可用性。

例如，使用这个特性来软删除。设置一个状态字段，在自定义的objects 中重写 get_queryset 来过滤状态。这样以后我们使用objects来查询model 的数据时，便会自动过滤状态。

```python

from django.db import models


class aManager(models.Manager):
    def get_queryset(self):
        return super(aManager, self).get_queryset().filter(isactive=True)


class A(models.Model):
    name = models.CharField(max_length=100)
    isactive = models.BooleanField()

    objects = aManager()

    def __unicode__(self):
        return '%s' % self.name


class B(models.Model):
    name = models.CharField(max_length=100)
    a = models.ForeignKey(A)

    def __unicode__(self):
        return '%s' % self.name
        
```

其他 管理器的使用可见 官方文档。


### 问题

今天遇到一个问题，如上的模型实例，数据如下：

![](/static/imgs/data-table.png)

通过 A 的关联条件查询 B 时，并没有过滤掉 A中状态。

如下：

![](/static/imgs/model-objects.png)

可以从 sql 看出，并没有对A 的状态进行过滤。

所以，此处注意。


### 结论

以后级联建议尽量使用唯一索引来过滤。



