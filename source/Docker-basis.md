---
layout : post
title : Docker学习笔记（一）--基础知识
category : docker
date : 2017-08-25
tags : [devops, 自动化运维, docker]
---

最近几年Docker容器技术已经渗透到各技术领域，在自动化运维领域更胜，因为它对于代码的部署上可以说是革命性的。下面是我学习Docker，记录的一些笔记，方便日后回忆备查。

<!-- more -->
## Docker 是什么

Docker 是一种轻量级的虚拟化技术，是一种Linux容器（Linux Containers，缩写为 LXC）技术的封装。

大多数人可能知道虚拟机，可以在一台硬件机器上虚拟出另一台计算机，有它自己的cpu、硬盘等各种虚拟的硬件。而 Linux 容器技术也是一种虚拟技术，但是它并非直接从硬件上来虚拟，而是通过软件技术对进程及资源进行隔离，从而达到虚拟化的目的。Docker 就是一种这样隔离虚拟化技术。

Docker的发展由来大致如下：

![](https://ws1.sinaimg.cn/large/8697aaedly1frtdhgj1ilj20k00dxaaj.jpg)

（图片来源：https://zhuanlan.zhihu.com/p/34732608）

Docker 与传统虚拟化技术不同如下：

![](https://ws1.sinaimg.cn/large/8697aaedly1frtfbkjvuxj211i0e0k14.jpg)

![](https://ws1.sinaimg.cn/large/8697aaedly1frtfbjwwm5j211g0aek1r.jpg)

(图片来源：Docker 从入门到实践)

## Docker 能做什么

Docker 可以做什么，从虚拟化角度来说，它可以完成如下功能：

- 隔离应用依赖
- 创建应用镜像并进行复制
- 创建容易分发的即启即用的应用
- 允许实例简单、快速地扩展
- 测试应用并随后销毁它们

Docker背后的想法是**创建软件程序可移植的轻量容器**

但是，对应整个软件开发流程来说，特别是测试和发布部署的意义非凡。

## Docker 优势

Docker 发展之迅速，除了分布式和微服务的大潮外，还得益于其优秀的特性。

**更高效的利用系统资源**

Docker 容器不需要进行硬件虚拟以及运行完整操作系统等额外开销，Docker 对系统资源的利用率更高。

**更快速的启动时间**

Docker 直接运行于宿主内核，无需启动完整的操作系统，因此可以做到秒级、甚至毫秒级的启动时间。大大的节约了开发、测试、部署的时间。

**一致的运行环境**

Docker 容器中有镜像的概念，Docker 容器有镜像生成，镜像保证了除内核外的运行环境。

**持续交付和部署**

也是因为镜像技术，可以使Devops人员实现持续集成、持续交付、部署，一次构建可在任意地方运行。

**更轻松的迁移**

Docker 容器封装了软件运行环境，使其不依赖系统，使其更容易移植。

**更轻松的维护和扩展**

Docker 使用分层存储和镜像技术，使得镜像可重复使用，维护和扩展更轻松。

**Docker相较虚拟机优势明显**

![](https://ws1.sinaimg.cn/large/8697aaedly1frtffbs8p2j21540aqq58.jpg)


## Docker 基本实现原理

Docker 的进程和资源隔离，基于 Linux 内核的cgroup，namespace，以及 AUFS 类的 Union FS 等技术实现的。

### NameSpace -- 资源隔离

- 充当隔离的第一级，确保一个容器中运行一个进程而且不能看到和影响容器外的其他进程。

### Cgroups(Control Group) -- 资源限制

- 限制Linux进程组的资源占用（内存、CPU）
- 为进程组制作 PID、UTS、IPC、网络、用户及装载命名空间

### UnionFS(Union 文件系统)

Union文件系统允许通过union装载来达到一个分层的积累变化。每个装载的文件系统表示前一个文件系统之后的变化集合，就像是一个diff。

![](https://ws1.sinaimg.cn/large/8697aaedly1frtflrag4kj20rf0aj3yz.jpg)


## Docker 核心概念

### 镜像

Docker 把应用程序及其依赖，打包在 image 文件里面。只有通过这个文件，才能生成 Docker 容器。image 文件可以看作是容器的模板。Docker 根据 image 文件生成容器的实例。同一个 image 文件，可以生成多个同时运行的容器实例。

Docker 通过 image 来分发转播。Docker 官方有维护的镜像仓库 [Docker Hub](https://hub.docker.com/),我们也可以搭建我们自己的镜像仓库，用来在企业内部使用。

镜像主要有如下特点：

- 类似虚拟机的快照，但更轻量，非常非常轻量。
- 镜像拥有唯一ID，以及一个供人阅读的名字和标签对。
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
 ![](https://ws1.sinaimg.cn/large/8697aaedly1frtflr73jlj20g9053mxd.jpg)

 ![](https://ws1.sinaimg.cn/large/8697aaedly1frtflr0c65j20jm0aggmn.jpg)

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


## docker 常用命令
```
1、 #从官网拉取镜像
docker pull <镜像名:tag>
如：docker pull centos(拉取centos的镜像到本机)
2、#搜索在线可用镜像名
docker search <镜像名>
如：docker search centos( 在线查找centos的镜像)
3、#查询所有的镜像，默认是最近创建的排在最上
docker images
4、#查看正在运行的容器
docker ps
5、#删除单个镜像
docker rmi -f <镜像ID>
docker rmi <name>:<tag>
6、#启动、停止操作
docker stop <容器名or ID> #停止某个容器 
docker start <容器名or ID> #启动某个容器 
docker kill <容器名or ID> #杀掉某个容器
7、#查询某个容器的所有操作记录。
docker logs {容器ID|容器名称} 
8、# 制作镜像  使用以下命令，根据某个“容器 ID”来创建一个新的“镜像”：
docker commit 93639a83a38e  wsl/javaweb:0.1
9、#启动一个容器
docker run -d -p 58080:8080 --name javaweb wsl/javaweb:0.1 /root/run.sh
解释：-d：表示以“守护模式”执行/root/run.sh脚本
          -p：表示宿主机与容器的端口映射，此时将容器内部的 8080 端口映射为宿主机的 58080 端口，这样就向外界暴露了 58080 端口，可通过 Docker 网桥来访问容器内部的 8080 端口了。
          -name:为容器命名
命令行启动：
docker run -it --rm ubuntu:14.04 bash
docker run 就是运行容器的命令，具体格式我们会在后面的章节讲解，我们这里简要的说明一下上面用到的参数。
* -it：这是两个参数，一个是 -i：交互式操作，一个是 -t 终端。我们这里打算进入 bash 执行一些命令并查看返回结果，因此我们需要交互式终端。
* --rm：这个参数是说容器退出后随之将其删除。默认情况下，为了排障需求，退出的容器并不会立即删除，除非手动 docker rm。我们这里只是随便执行个命令，看看结果，不需要排障和保留结果，因此使用 --rm 可以避免浪费空间。
* ubuntu:14.04：这是指用 ubuntu:14.04 镜像为基础来启动容器。
* bash：放在镜像名后的是命令，这里我们希望有个交互式 Shell，因此用的是 bash。

10、#最后补充一个启动docker服务的命令
很简单：
service docker start

11、删除容器
docker rm $(docker ps -a -q)

12、进入后台运行的docker容器
docker attach 5ac094c371f5
docker exec -it liBlog-db bash


```

## Docker 其他知识点

### Docker for Mac 的安装路径
/Users/{YourUserName}/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/Docker.qcow2

### Docker镜像的可移植性

- Docker允许你在一个镜像中指定卷和端口。从这个镜像创建的容器继承了这些设置。但是，Docker不允许你在镜像上指定任何不可移植的内容。

###  docker 相关文档收集

- [images 保存路径 及说明](http://blog.csdn.net/wanglei_storage/article/details/50299491)
- [docker 镜像与容器存储目录结构精讲](http://blog.csdn.net/wanglei_storage/article/details/50299491)
- [深入理解Docker的link机制](https://blog.csdn.net/zhangyifei216/article/details/50921215)
- [docker运行nginx为什么要使用 daemon off](https://segmentfault.com/a/1190000009583997)
- [CMD ENTRYPOINT 区别](https://blog.csdn.net/u010900754/article/details/78526443)
- [容器如何连接宿主机服务（mysql）](https://stackoverflow.com/questions/24319662/from-inside-of-a-docker-container-how-do-i-connect-to-the-localhost-of-the-mach/24326540%2324326540)

## 参考

- [Docker 从入门到实战（第二版）](https://legacy.gitbook.com/book/yeasy/docker_practice/details)
- [docker终极指南](http://dockone.io/article/133)
- [Docker三年回顾：梦想依在，人生正当年](http://www.infoq.com/cn/articles/docker-turns-3)
