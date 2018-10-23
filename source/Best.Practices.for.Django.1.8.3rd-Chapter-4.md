---
layout : post
title : Django 最佳实践-读书笔记 - 第四章 django app的设计
category : django
date : 2016-05-22
tags : [django]
---

[其他章节索引页](2016-05-22-Best.Practices.for.Django.1.8.3rd-Index.html)

# 第四章 django app的设计

## Django的 app 设计的黄金法则

- each app should be tightly focused on its task.
（每个 app 的功能任务尽量的独立分开，这样能更好的重用。）

## 如何命名你的 app 

- 使用app中主 model 的名称复数形式 
- 使用有效，PEP 8兼容，无简写，全小写名称，数字，破折号，句点，空格或特殊字符。如果为了便于阅读，你可以使用下划线分割。
<!-- more -->

## 尽量使你的 app 变小。

