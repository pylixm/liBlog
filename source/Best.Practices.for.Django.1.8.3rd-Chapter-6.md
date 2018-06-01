---
layout : post
title : Django 最佳实践-读书笔记 - 第六章 model 最佳实践
category : django
date : 2016-05-22
tags : [django]
---


[其他章节索引页](2016-05-22-Best.Practices.for.Django.1.8.3rd-Index.html)

# 第六章 model 最佳实践

## 当app的model过多时，拆分app

当app的model过多时，说明这个app的功能够大，此时就需要我们拆分app了。

## 模型继承的使用

- 抽象基类（区别django的抽象基类和python的抽象类）
- 多表继承（尽量不要使用，效率低下）
- 代理模式

## 数据模型的规范化

同数据库设计的规范化，推荐阅读：

- http://en.wikipedia.org/wiki/Database_normalization
- http://en.wikibooks.org/wiki/Relational_Database_Design/Normalization
 
## 使用 Null 和 Blank时注意

在字段上设置null=True 和 the blank=True，他们默认是False。

## 使用 GenericIPAddressField 代替IPAddressField，后者将要移除。

## 使用 BinaryField 字段注意

- django 1.8 增加了存储二进制的字段类型。当存储大容量二进制值，成为系统存储瓶颈时，可将二进制值放到文件中，使用 filefield 字段类型来解决。

- 不要用这个字段存储文件。
  原因：
  - 访问数据库，没有访问文件块
  - 备份数据库，耗时增加
  - 去访问文件，需要通过你的django app 。


## 尽量避免使用通用关联关系

- 加快查询速度
- 减少数据损坏造成的关联数据的问题


## 善于使用meta

## 自定义manager管理器时注意

- 抽象基类中，子类不能继承父类的 manager 
- 会造成不能预知的问题
- `objects = models.Manager()` 放在所有自定义管理器的前边。


## 理解“Fat models”

- model behaviors 利用model的继承（抽象基类）特性实现。将model的部分属性或方法提取到一个Mixins中，通过继承来共用。 参考：
http://blog.kevinastone.com/django-model-behaviors.html

- 辅助函数的使用。抽象对模型的重复操作，放到utility 函数中作为模型辅助函数。
