---
layout : post
title : Docker学习笔记--基础知识
category : docker
date : 2017-08-25
tags : [devops, 自动化运维, docker]
---

## Docker 能做什么

- 隔离应用依赖
- 创建应用镜像并进行复制
- 创建容易分发的即启即用的应用
- 允许实例简单、快速地扩展
- 测试应用并随后销毁它们

Docker背后的想法是**创建软件程序可移植的轻量容器**


## Docker 基本实现原理

### NameSpace -- 资源隔离

- 充当隔离的第一级，确保一个容器中运行一个进程而且不能看到和影响容器外的其他进程。

### Cgroups(Control Group) -- 资源限制

- 限制Linux进程组的资源占用（内存、CPU）
- 为进程组制作 PID、UTS、IPC、网络、用户及装载命名空间

### UnionFS(Union 文件系统)

Union文件系统允许通过union装载来达到一个分层的积累变化。每个装载的文件系统表示前一个文件系统之后的变化集合，就像是一个diff。

![image](http://dockerone.com/uploads/article/20150109/80f162ad554833229628f1753cd501d0.png)

## Docker 核心概念

### 镜像

- 类似虚拟机的快照，但更轻量，非常非常轻量。

- 镜像拥有唯一ID，以及一个供人阅读的名字和标签对

- 只读层被称为镜像，一个镜像是永久不会变的。

- 由于 Docker 使用一个统一文件系统，Docker 进程认为整个文件系统是以读写方式挂载的。 但是所有的变更都发生顶层的可写层，而下层的原始的只读镜像文件并未变化。由于镜像不可写，所以镜像是无状态的。

### 容器

- 你可以从镜像中创建容器，这等同于从快照中创建虚拟机，不过更轻量。
- 应用是由容器运行的。
- 拥有一个唯一ID和唯一的供人阅读的名字
- Docker允许公开容器的特定端口。
- 容器被设计用来运行单进程，Docker设计者极力推崇“一个容器一个进程的方式”。
- 容器应该是短暂和一次性的。

容器和镜像
 ![image](http://dockerone.com/uploads/article/20150109/7e456b0341559afa06a6076625c4edde.png)

 ![image](http://dockerone.com/uploads/article/20150109/a846617cf45d4ccc36d907ef40abe592.png)
 
### 数据卷

- 数据卷让你可以不受容器生命周期影响进行数据持久化。
- 它们表现为容器内的空间，但实际保存在容器之外，从而允许你在不影响数据的情况下销毁、重建、修改、丢弃容器。
- Docker允许你定义应用部分和数据部分，并提供工具让你可以将它们分开。
- 使用Docker时必须做出的最大思维变化之一就是：**容器应该是短暂和一次性的。**

![image](http://dockerone.com/uploads/article/20150109/16069b19876f5e59a5d0e77a7053fff3.png)

### 链接

- Docker允许你在创建一个新容器时引用其它现存容器，在你刚创建的容器里被引用的容器将获得一个（你指定的）别名。我们就说，这两个容器链接在了一起。
- ![image](http://dockerone.com/uploads/article/20150109/9b6c96106a808c09988fb60f777ddad2.png)

如果DB容器已经在运行，我可以创建web服务器容器，并在创建时引用这个DB容器，给它一个别名，比如dbapp。在这个新建的web服务器容器里，我可以在任何时候使用主机名dbapp与DB容器进行通讯。

## Docker镜像的可移植性

- Docker允许你在一个镜像中指定卷和端口。从这个镜像创建的容器继承了这些设置。但是，Docker不允许你在镜像上指定任何不可移植的内容。


## 参考

- [docker终极指南](http://dockone.io/article/133)