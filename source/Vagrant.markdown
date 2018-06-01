---
layout : post
title : vagrant、docker、virtualbox之间的区别
category : 虚拟机
date : 2015-11-29 22:22:00
tags : [容器, 虚拟机]
---



同事推荐了一个虚拟机管理的工具 vagrant ，查了下发现果然不错。试着装了下，看安装说明，需要装virtualbox。也是一个虚拟机软件，和VMware
有点类似。遂查了下几个名词的区别，顺便和当下流行的容器 docker 的区别一并查了下，简单记录如下：

### virtualbox 

VirtualBox 是一款开源虚拟机软件。VirtualBox号称是最强的免费虚拟机软件，它不仅具有丰富的特色，而且性能也很优异！它简单易用，
可虚拟的系统包括Windows（从Windows 3.1到Windows10、Windows Server 2012，所有的Windows系统都支持）、Mac OS X、
Linux、OpenBSD、Solaris、IBM OS2甚至Android等操作系统。



### docker

Docker 是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的 Linux 机器上，
也可以实现虚拟化。容器是完全使用沙箱机制，相互之间不会有任何接口（类似 iPhone 的 app）。
几乎没有性能开销,可以很容易地在机器和数据中心中运行。最重要的是,他们不依赖于任何语言、框架包括系统。


### vagrant 

Vagrant是一个基于Ruby的工具，用于创建和部署虚拟化开发环境。它 使用Oracle的开源VirtualBox虚拟化系统，
使用 Chef创建自动化虚拟环境。

---

### virtualbox 和docker 比较 

- 1、virtualbox，是创建硬件虚拟化的软件，类似于vmware。Docker，则是不进行硬件的虚拟化，Docker虚拟化操作系统。

- 2、virtualbox，通常情况下，一个操作系统运行在硬件上，其中硬件和操作系统之间的通信是通过移动数据到内存地址，
    然后发出指令来通知可使用该数据的硬件（或者是数据在被读取时）。 在VirtualBox（或其它虚拟机）设置的环境中，
    那些内存地址实际上是虚拟机软件自身的内存区域，并且那些指令是由虚拟机而不是直接由底层的CPU解释的。实际结果是，
    你在VirtualBox中运行一个操作系统，对于这个操作系统来说，VirtualBox程序看起来像一台完整计算机，硬件以及所有配件都有。
    实际上它不知道自己是在另一个程序中运行的。

- 3、Docker，它的作用是创建一个文件系统，使其看起来像一个普通的Linux文件系统，并且运行应用程序在一个所有文件和资源都在文件系统内的锁定环境中。
  事实上，该应用程序的容器并不模仿任何硬件，应用程序仍然在硬件上运行，它只是隔离了应用程序并允许您可以运行该应用程序跟特定的并且完全
  不是主机操作系统的软件和第三方库合作。这意味着，在启动或停止Docker应用程序时几乎没有开销，因为它们不需要预先分配的内存和磁盘
  空间等等。因此Docker容器很容易设置或者拆除。此外，容器在假装需要系统中各种硬件组件上运行软件的时候并不浪费任何开销 - 它是直接使用
  硬件的。
  
### vagrant 和 docker 比较

针对 vagrant 和docker的区别，docker的作者Hykes有这样的观点。

>如果你仅仅是想管理虚拟机，那么你应该使用vagrant。如果你想快速开发和部署应用，那么应该使用docker。
vagrant是一款管理虚拟机的工具，而docker是一款通过将应用打包到轻量级容器，而实现构建和部署的工具。

最后可以说：Vagrant 适合用来管理虚拟机，而docker适合用来管理应用环境。

--- 

#### 参考

* [http://www.aixchina.net/home/space.php?uid=59140&do=blog&id=136449](http://www.aixchina.net/home/space.php?uid=59140&do=blog&id=136449)

* [http://www.linuxidc.com/Linux/2014-09/106783.htm](http://www.linuxidc.com/Linux/2014-09/106783.htm)
