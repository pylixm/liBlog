---
layout : post
title : 译 - 在pycharm中使用docker
category : docker
date : 2017-10-29
tags : [devops, 自动化运维, docker]
---

>*update：2018-05-31*
>本文针对 `Pycharm2017.3`。
>最近在学习docker，作为一个pycharm重度使用者，很想知道怎么在pycharm里使用docker,看到官博的这2片文章不错，摘录翻译备查。水平有限，还请批评指正！

现在的开发工作流程中，强调开发和生产中的隔离和再现性。 Docker和容器平台技术已经变得非常受欢迎。 现在 PyCharm 已支持Docker作为远程解释器使用。

让我们来看看在pycharm中，docker是如何使用的：
- 获取针对Django的Docker镜像。
- 做一个Django示例项目
- 创建一个Docker解释器来运行项目
- Django运行配置在启动时创建一个新容器，并在停止时将其移除

<!-- more -->
## 概述

在Python中，当您运行应用程序时，Django站点，数据库脚本等 - 您需要一个环境来运行它。 Python具有管理环境并使其可重复的工具，例如virutal environment，pip require.txt文件和setup.py依赖项。 但是应用程序的非Python部分呢？

容器是一个解决方案。 在Docker中，容器是一个运行在计算机内部的，独立的，运行着各种软件的空间。 它们可以快速且很容易地创建，开始，停止和销毁。 这是理想的，不仅仅是为了开发，还有部署。


## 准备

首先，确保您的环境中设置了docker和docker-machine。 Docker安装是无痛的，网站文档相当友好。 您将需要一个Docker“主机”虚拟机的安装和运行，包括在Linux上。 在Windows和OS X上，安装Docker Toolbox是免费的。

接下来，我们必须在我们的容器中确定我们想要什么软件。 在Docker中，容器使用“images”构建：预先安装的软件集合以及在容器创建过程中调用的配置。 与PyCharm中的其他解释器不同，您不必访问Project Interpreter首选项以添加Python依赖包，所有的python依赖项都需要放入您选择的Docker镜像中。

django的docker开发环境可以基于`minimum/docker-django-mysite`镜像，其中包含足够的Python/Django软件来运行PyCharm生成的Django启动项目。 您可以使用以下命令将其提取到系统上：

```bash
$ docker pull minimum/docker-django-mysite
```

一旦Docker镜像在本地可用，PyCharm便可为您的项目创建基于该映像的Docker容器作为python解释器使用。

或者，您可以跳过此步骤，在创建基于Docker的远程解释器时，键入镜像名称拉取镜像使用。

注意：您可以选择使用Dockerfile制作自己的镜像。 一旦你制作镜像，PyCharm便可根据它做Docker解释器。


## 开始使用

### 创建django项目

让我们创建一个Django项目，然后为它设置一个Docker解释器。 在PyCharm中，选择File - >create new project，单击Django，并按照正常的进程制作Django项目。

`在创建项目期间，您必须使用 local interpreter。 如果您尝试制作 Docker interpreter，PyCharm会发出警告，指出您只能使用 local interpreter。`

此步骤的结果是本地计算机上的一个目录，其中包含示例Django代码和Django特定的PyCharm运行配置。

### 配置一个docker interpreter，运行项目

- 1、到`Preferences -> Project Interpreter -> Add Romete `，选择本地的可用Docker 镜像,如图：
![](/static/imgs/docker-config-1.png)

- 2、配置`Edite configrations`, 将host设置为`0.0.0.0`, 选择刚才添加的项目解释器，并配置容器运行参数`Docker container settings`，如图：
![](/static/imgs/docker-config-2.png)

说明：
- 容器端口：8000 映射到主机端口 80
- 挂载项目目录的数据卷： ` /Users/pylixm/docker.dev/django-demo/mysite:/code/mysite`

- 3、正常启动项目，访问`http://0.0.0.0:80`,即可看到亲切的欢迎界面。


### pycharm 在运行时，会做什么

- 它会基于我们选择的项目解释器的docker镜像创建并启动一个新的容器。
- 此容器将您的项目目录装载到容器中 `/opt/project`的容器中。 注意：在Linux上，您当前必须手动执行此卷映射。 
- 此容器还安装PyCharm所需的卷以完成其工作：Python骨架和Python库源。
- 然后执行运行配置的Python命令。


## 使用 docker-compose 

编写好 compose 配置文件，可参考 [https://github.com/pydanny/cookiecutter-django/](https://github.com/pydanny/cookiecutter-django/)。
pycharm 项目解释器选择如下：
![](/static/imgs/docker-compose-pycharm.png)

当 compose 配置服务太多时，构建可能比较慢。可参考官博上的[flask实例](https://github.com/ErnstHaagsman/flask-compose/blob/master/docker-compose.dev.yml)，查看运行情况。



## 参考

- [https://blog.jetbrains.com/pycharm/2015/12/using-docker-in-pycharm/](https://blog.jetbrains.com/pycharm/2015/12/using-docker-in-pycharm/)
- [https://blog.jetbrains.com/pycharm/2017/03/docker-compose-getting-flask-up-and-running/](https://blog.jetbrains.com/pycharm/2017/03/docker-compose-getting-flask-up-and-running/)