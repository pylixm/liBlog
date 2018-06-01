---
layout : post
title : Django 最佳实践-读书笔记 - 第二章  django 环境配置
category : django
date : 2016-05-22
tags : [django]
---


[其他章节索引页](2016-05-22-Best.Practices.for.Django.1.8.3rd-Index.html)

# 第二章  django 环境配置

## 使用相同的数据库引擎配置

在不同的环境下使用不同的数据库，而希望其行为一致。这种做法是很危险的，会带来不可预知的问题。

问题：

- 生产数据不能够精确的恢复到本地
- 不同数据库的字段的类型和约束行为不同
- Fixtures 并不是万能的解决方案。请不要使用它来迁移生产数据。


## 使用 Pip 和 Virtualenv

pip : python 包管理工具，方便的安装和卸载python 三方库包。

virtualenv : python 孤立的运行环境，可以将不同版本的 python 三方包分离，当需要的时候切换。

virtualenvwrapper ：Virtualenvwrapper is a popular companion tool to pip and virtualenv and makes our lives
easier, but it’s not an absolute necessity.

## 使用 pip 安装django和开发依赖包

## 使用版本控制软件

推荐：

- git 
- Mercurial


## 尽量保证开发和生产环境的一致性

- 可以使用 Vagrant and VirtualBox 来虚拟生产环境。
