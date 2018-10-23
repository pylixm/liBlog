---
layout : post
title : 转-saltstack 中Grains 与pillar的区别
category : salt
date : 2016-09-04
tags : [salt]
---

原文地址：http://www.aikaiyuan.com/9728.html

grains类似于puppet的facter！facter是用来收集客户的信息的，
pillar相当于puppet的Hiera！Hiera用来组织变量，结构化变量！
grains类似于puppet的facter 是用来探测出minion的一些变量，比如主机名，内存大小，IP地址，系统及版本号等。相对来说，grains存储的是静态/不常变化的内容
<!-- more -->
而pillar作为salt中独立的系统，个人认为是配置管理的精髓，其信息是存储在master上或其他扩展的后端，如mongodb等，结合SLS，通过pillar传送对应的配置管理变量(如需要安装的软件版本，安装位置，配置文件参数，防火墙规则等)实现一套SLS即可完成各种需求的状态配置.

grains和pillar的另一个区别就是grains是存储在minion本地，所以grains可以进行新增、变更、删除等操作(通过grains模块append、remove、setval、delval等方法); 而pillar是存储在master本地或者第三方平台上，minion只能查看自己的，没有权限做新增、变更、删除操作。


1.grains存储的是静态、不常变化的内容，pillar则相反
2.grains是存储在minion本地，而pillar存储在master本地
3.minion有权限操作自己的grains值，如增加、删除，但minion只能查看自己的pillar，无权修改