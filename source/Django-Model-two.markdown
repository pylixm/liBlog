---
layout : post
title : Django学习笔记-模型(2)模型的操作
category : django
date : 2015-11-13
tags : [django,]
---



## 二、模型的操作（QuerySets）

### 1、模型操作基础

**常用接口方法**

- all(): 返回一个包含模式里所有数据记录的结果集queryset 
- filter():返回一个包含符合指定条件的模型记录的queryset
- exclude():和filter相反 查找不符合条件的那些记录
- get():获取单个复核条件的记录（没有找到或有超过一个结果都会抛出异常）
- order_by(): 排序

**queryset的查询及符号**

```python
queryset.distinct 
queryset.values()
quetyset.values_list()
queryset.select_related()
queryset.filter(title__gt='123')
querySet.distinct()  #去重复
__exact       # 精确等于 like 'aaa'
__iexact   # 精确等于 忽略大小写 ilike 'aaa'
__contains  #  包含 like '%aaa%'
__icontains #  包含 忽略大小写 ilike '%aaa%'，
# 但是对于sqlite来说，contains的作用效果等同于icontains。
__gt    #大于
__gte   # 大于等于
__lt    #小于
__lte   # 小于等于
__in    # 存在于一个list范围内
__startswith   #以...开头
__istartswith #  以...开头 忽略大小写
__endswith    # 以...结尾
__iendswith   # 以...结尾，忽略大小写
__range   # 在...范围内
__year    #   日期字段的年份
__month   # 日期字段的月份
__day      #  日期字段的日
__isnull=True/False
```

**实例**

```python
>>> Publisher.objects.filter(country="U.S.A.", state_province="CA")
[<Publisher: Apress>]
# 逗号表示，and
>>> Publisher.objects.filter(name__contains="press")
[<Publisher: Apress>]
```
### 2、模型的操作

#### 2.1 对象创建：

```python
>>> p = Publisher(name='Apress',
...         address='2855 Telegraph Ave.',
...         city='Berkeley',
...         state_province='CA',
...         country='U.S.A.',
...         website='http://www.apress.com/')
>>> p.save()
```
#### 2.2 对象更新：

*方法1*：

```python
>>> Publisher.objects.filter(id=52).update(name='Apress Publishing')
# update()方法会返回一个整型数值，表示受影响的记录条数。
```

*方法2*：

```python
>>> pub= Publisher.objects.filter(id=52).first()
>>> pub.name = 'Apress Publishing'
>>> pub.save()
```

<font color='red'>注：1方法更优，2方法会更新publisher 的所有字段，所以效率低。</font>

#### 2.3 删除对象：

*单条*

```python
>>> p = Publisher.objects.get(name="O'Reilly")
>>> p.delete()
>>> Publisher.objects.all()
[<Publisher: Apress Publishing>]
```

*多条*

```python
>>> Publisher.objects.filter(country='USA').delete()
>>> Publisher.objects.all().delete()
>>> Publisher.objects.all()
[]
```

三、模型的迁移

    # todo

四、模型的高级特性

    # todo 

五、其他

    # todo 
    
    
#### 参考：

[https://docs.djangoproject.com/en/1.8/topics/db/queries/](https://docs.djangoproject.com/en/1.8/topics/db/queries/)

