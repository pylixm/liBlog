---
layout : post
title : Django 最佳实践-读书笔记 - 第七章 查询与数据库层
category : django
date : 2016-06-19 22:00:00
tags : [django]
---


[其他章节索引页](2016-05-22-Best.Practices.for.Django.1.8.3rd-Index.html)

# 第七章 查询与数据库层

## 查询单个对象时，使用 get_object_or_404()

注意，此函数仅在你的 views 中使用。切勿在 helper functions, forms, model methods or anything that is not a view
or directly view related 使用。

## 在可能报错的查询段，增加 try-except

- 查询对象不存在 ：ObjectDoesNotExist vs. DoesNotExist
- 查询一个对象，返回多条时：MultipleObjectsReturned

## 列用django orm 的惰性机制，使查询代码变的清晰、可读性更高

```python
results = results.filter(
Q(name__startswith=name) |
Q(description__icontains=name)
)
results = results.exclude(status='melted')
results = results.select_related('flavors')

```

## 高级查询的使用

- django orm 的高级查询表达式
  - Customer.objects.iterate()
  - 详见：https://docs.djangoproject.com/en/1.8/ref/models/expressions/
  
  
- django orm 的数据库函数应用
  - `Author.objects.update(alias=Lower(Substr('name', 1, 5)))` 更多 UPPER(),LOWER(), COALESCE(), CONCAT(), LENGTH(), and SUBSTR()
  - 详见：https://docs.djangoproject.com/en/1.8/ref/models/database-functions/ 
  
## 当裸sql不是必须的时候，不要使用

缺点：
- 降低 django app 的可移植性

但是，有时候，写裸sql是必须的，那就去勇敢的写。

django 核心开发者  Malcolm Tredinnick 说：

> “Django ORM can do many wonderful things, but sometimes SQL is the right
answer. The rough policy for the Django ORM is that it’s a storage layer that
happens to use SQL to implement functionality. If you need to write advanced
SQL you should write it. I would balance that by cautioning against overuse of
the raw() and extra() methods.”

所以说，2者有机的结合使用，才是最佳实践。

## 在orm 中增加索引，它会加快你的查询。

`db_index=True`

## 在一个工作单元中完成多个数据库操作，使用事务管理（Transaction）

- 全局request事务 
```
DATABASES = {
  'default': {
    # ...
    'ATOMIC_REQUESTS': True,
  },
}
```
- `@transaction.non_atomic_requests` 使用它来关闭request事务。
 
- 使用显示的事务声明，来减小全局事务的性能开销。

- 不要试着去包装 model 的[.create(), .update(),.delete()] 方法，这样会失去其内部的事务调用。