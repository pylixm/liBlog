---
layout : post
title : Django学习笔记-模型(1)模型的定义
category : django
date : 2015-11-01
tags : [django,]
---


　　Django也遵循了MVC的分层原则，不过在做法上略有不同。首先模型部分保持不变：Django的模型增只负责把数据传入传出数据库。然而Django里的视图却并不是显示数据的最后一步。Django的视图其实更接近MVC里传统意义上的控制器。他们是用来将模型层和表示层（有HTML和Django的模板语言组成）链接在一起的python函数。

　　按Django开发团队的话老说就是： 我们理解的MVC里，视图的作用是描述将要显示给用户的数据。这不仅仅是数据看上去的外观，含包括如何表示数据。视图描述的是你能看那些数据，而不是怎么看到它。

　　换一种说法，Django把表示层一分为二，视图方法定义了要显示模型里的什么数据，而模板则定义了最终信息的显示方式。而框架自己则担当了控制器的角色--它提供了决定什么视图和什么模板一起响应给定请求的机制。


## 一、模型的定义

### 1、基础：

    - 每个模型都是django.db.models.Model 的一个Python 子类。
    - 模型的每个属性都表示数据库中的一个字段。
    - Django 提供一套自动生成的用于数据库访问的API；
    - 模型表名为 myapp_modelname 

### 2、字段

**django常见Field Types：**

1. `AutoField`
如果没有指明主键，就会产生一个自增的主键。
2. `BigIntegerField`
64位的整型数值，从 -2^63 (-9223372036854775808) 到 2^63-1(9223372036854775807)。
3. `BinaryField`
存储原始二进制数据，仅支持字节分配。功能有限。
4. `BooleanField`
布尔型和NullBooleanField有区别，true/false，本类型不允许出现null。
5. `CharField`
字符串，一般都在创建时写入max_length参数。
6. `CommaSeparatedIntegerField`
逗号分隔的整数，考虑到数据库的移植性，max_length参数应该必选。
原文解释：A field of integers separated by commas. As in CharField, the max_length argument is required and the note about database portability mentioned there should be heeded.
7. `DateField`
时间，对应Python的datetime.date，额外的参数：DateField.auto_now表示是否每次修改时改变时间，DateField.auto_now_add 表示是否创建时表示时间，一般来说数据库重要的表都要有这样的字段记录创建字段时间个最后一次改变的时间。关于时间的话，建议timestamp，当然 python的话还是DateTime吧。
8. `DateTimeField`
对应Python的datetime.datetime，参照参数（7）。
9. `DecimalField`
固定精度的十进制数，一般用来存金额相关的数据。对应python的Decimal，额外的参数包括DecimalField.max_digits和DecimalField.decimal_places ，这个还是要参照一下mysql的Decimal类型，http://database.51cto.com/art/201005/201651.htm
例如：price = models.DecimalField(max_digits=8,decimal_places=2)
10. `EmailField`
字符串，会检查是否是合法的email地址
11. `FileField`
class FileField([upload_to=None, max_length=100, **options])
存文件的，参数upload_to在1.7之前的一些老版本中必选的
12. `FloatField`
浮点数，必填参数：max_digits，数字长度；decimal_places，有效位数。
13. `ImageField`
class ImageField([upload_to=None, height_field=None, width_field=None, max_length=100, **options])
图片文件类型，继承了FileField的所有属性和方法。参数除upload_to外，还有height_field，width_field等属性。
14. `IntegerField`
[-2147483648,2147483647 ]的取值范围对Django所支持的数据库都是安全的。
15. `IPAddressField`
点分十进制表示的IP地址，如10.0.0.1
16. `GenericIPAddressField`
ip v4和ip v6地址表示，ipv6遵循RFC 4291section 2.2,
17. `NullBooleanField`
可以包含空值的布尔类型，相当于设置了null=True的BooleanField。
18. `PositiveIntegerField`
正整数或0类型，取值范围为[0 ,2147483647]
19. `PositiveSmallIntegerField`
正短整数或0类型，类似于PositiveIntegerField，取值范围依赖于数据库特性，[0 ,32767]的取值范围对Django所支持的数据库都是安全的。
20. `SlugField`
只能包含字母，数字，下划线和连字符的字符串，通常被用于URLs表示。可选参数max_length=50，prepopulate_from用于指示在admin表单中的可选值。db_index，默认为True。
21. `SmallIntegerField`
小整数字段，类似于IntegerField，取值范围依赖于数据库特性，[-32768 ,32767]的取值范围对Django所支持的数据库都是安全的。
22. `TextField`
文本类型
23. `TimeField`
时间，对应Python的datetime.time
24. `URLField`
存储URL的字符串，默认长度200；verify_exists(True)，检查URL可用性。
25. `FilePathField`
class FilePathField(path=None[, match=None, recursive=False, max_length=100, **options])
类似于CharField，但是取值被限制为指定路径内的文件名，path参数是必选的。

*详见官方文档*：
https://docs.djangoproject.com/en/1.8/ref/models/fields/#field-types

**常用字段属性**

- null
如果设置为 True , Django 存放一个 NULL 到数据库字段。默认为 False。

- blank
如果设置为 True , 此 field 允许为 blank （空白），默认为 False。
要注意，这与 null 不同。null纯粹是数据库范畴的，而 blank 是数据验证范畴的。如果一个字段的blank=True，表单的验证将允许该字段是空值。如果字段的blank=False，该字段就是必填的。
- choices
一个2元元组的元组或者列表，如果执行 choices ， Django 的 admin 就会使用 选择框而不是标准的 text 框填写这个 field。

- default
field 的默认值，可以使用可调用对象（a callable object），如果使用可调用 对象，那么每次创建此 model 的新对象时调用可调用对象。常见如 datatime 。

- help_text
help_text 的值可以在 admin form 里显示，不过即使不使用 admin ，也可以当 做描述文档使用。

- primary_key
如果为 True ， 这个 field 就是此 model 的 primary key 。

- unique
如果为 True， 此 field 在这个 table 里必须唯一。
- verbose_name
ForeignKey、ManyToManyField 和 OneToOneField 使用此来定义“自述名”。

### 3、关系

- 多对一 ： ForeignKey
- 多对多 ：ManyToManyField 可以自定义中介模型，源模型的ManyToManyField 字段将使用through 参数指向中介模型
- 一对一 ：OneToOneField 

### 4、模型继承

- 通常，你只想使用父类来持有一些信息，你不想在每个子模型中都敲一遍。这个类永远不会单独使用，所以你使用抽象基类。
- 如果你继承一个已经存在的模型且想让每个模型具有它自己的数据库表，那么应该使用多表继承。
- 最后，如果你只是想改变模块Python 级别的行为，而不用修改模型的字段，你可以使用代理模型。
    
    
#### 参考：

[https://docs.djangoproject.com/en/1.8/topics/db/models/](https://docs.djangoproject.com/en/1.8/topics/db/models/)