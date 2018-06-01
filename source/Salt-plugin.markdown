---
layout : post
title : Saltstack学习笔记-组件篇
category : salt
date : 2016-08-21
tags : [salt]
---


## saltstack 架构

saltstack 是基于python开发的一套 c/s架构配置管理工具。底层使用ZeraMQ消息队列的发布与订阅（pub/sub）方式通信，使用SSL证书签发的方式进行认证管理。

## saltstack 组件

### 管理对象 Target 

target 匹配，

    -E , --pcre 正则匹配
    -L , --list 列表匹配
    -G , --grain grains值匹配
    --gran-pcre grains加正则
    -N , --nodegroup 组匹配
    -R , --range 范围匹配
    -C , --compound 综合匹配
    -I , --pillar pillar 值匹配
    -S , --ipcidr minions 网段匹配
    
### Grains 组件

grains 组件是saltstack记录minion的一些静态信息的组件。

    # 查看Grains组件的函数
    salt '*' sys.list_functions grains 
    
    # 查看具体函数的使用方法
    salt '*' sys.doc grains 
    
除了自带的grains外，还可以自己定义，定义方法：

- 通过minion 配置文件，将Grains信息配置写在minion配置文件中。
- 通过grains 相关模块定义，使用Grains 模块添加或删除grains信息。
- 通过python 脚本定义


### Pillar 组件

pillar 用来存储和定义配置管理中需要的一些信息。

    # 查看pillar组件的函数
    salt '*' sys.list_functions pillar 
    
    # 查看具体函数的使用方法
    salt '*' sys.doc pillar
    
### Module 组件

用来管理对象操作，是saltstack通过push方式管理的入口。

    # 查看所有modules
    salt '*' sys.list_modules
    # 查看具体module的函数
    salt '*' sys.list_functions cmd 
    # 查看module的用法
    salt '*' sys.doc cmd
    
    
### States 组件

states sls 文件用来描述和实现配置管理的功能。

    # 查看所有states
    salt '*' sys.list_states_modules
    # 查看具体states的函数
    salt '*' sys.list_states_functions file
    # 查看states的用法
    salt '*' sys.state_doc file


### Return 组件

对minion执行的返回结果进行存储或返回给其他程序。

    # 查看所有return 
    salt '*' sys.list_returners

目前saltstack 以支持master和minion端，两种方式return数据到存储服务器。

### job 

saltstack 执行任何一个操作都会在Master上产生一个jid号。master和minion会产生一jid命名的job文件，里面存了此次操作的详细信息。

job管理的方式：

- `salt-run` 
- salt自带模块 `saltutil`


### Event 和Reactor 

event 是对每个事件的一个记录，比job更底层，更加详细。包括认证、minion和master 的链接，key认证，job等。

- `salt-run state.event pretty=True` 查看event事件

reactor 是对event的监听，基于event的事件来做相应的操作。


### Renderer

renderer 是编写state.sls 文件的途径的统一称呼。默认的renderer语法是YAML+ jinja。

比较流行的方式：

- python 
- yaml
- jinja







