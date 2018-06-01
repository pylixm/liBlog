---
layout : post
title : Docker学习笔记--简单使用记录
category : docker
date : 2017-08-26
tags : [devops, 自动化运维, docker]
---

## 安装 

docker 安装现在已非常简单，具体可参考[官方文档](https://docs.docker.com/engine/installation/).

安装成功后可以使用以下命令检测：
```bash
$ docker --version
Docker version 17.06.2-ce, build cec0b72

$ docker-compose --version
docker-compose version 1.14.0, build c7bdf9e

$ docker-machine --version  # 在windows 和mac os 上管理docker容器 
docker-machine version 0.12.2, build 9371605
```
注：
1、`docker-machine` [文档介绍](https://docs.docker.com/machine/overview/)
2、`docker-compose` 官方docker容器编排工具，[文档介绍](https://docs.docker.com/compose/overview/)
3、更换docker 源，[官方文档](https://docs.docker.com/registry/recipes/mirror/#use-case-the-china-registry-mirror),[网友文档](http://www.jianshu.com/p/9fce6e583669)


## Docker 使用案例：使用docker 来搭建python开发环境 

docker 容器的运行是基于docker镜像的，所以我们需要先获取镜像。镜像的获取有几种方法：
- 1、从docker cloud 上拉取所需要的镜像，修改打包使用。
- 2、自己编写Dockerfile, 基于现有镜像，自己构建新镜像。

### 第一步，镜像获取

我们这里通过编写Dockerfile来定制镜像。
```dockerfile
FROM python:2.7  
ENV PYTHONUNBUFFERED 1  
RUN mkdir /code    
WORKDIR /code  
ADD ./requirements.txt /code/  
RUN pip install -r requirements.txt  
```
>说明：
> - 1、依据python:2.7 镜像构建
> - 2、这是python环境变量
> - 3、在docker容器内创建代码目录
> - 4、设置工作目录为 code 
> - 5、复制文件到code 目录下
> - 6、执行命令安装python依赖包

注：
1、如何编写Dockerfile, [官方文档](https://docs.docker.com/engine/reference/builder/)
2、copy vs add [官方文档](https://docs.docker.com/engine/reference/builder/#copy)，[网友解释](http://blog.csdn.net/liukuan73/article/details/52936045)

>ADD 功能更多：
>- ADD指令可以让你使用URL作为<src>参数。当遇到URL时候，可以通过URL下载文件并且复制到<dest>。
>- ADD的另外一个特性是有能力自动解压文件。如果<src>参数是一个可识别的压缩格式（tar, gzip, bzip2, etc）的本地文件（所以实现不了同时下载并解压），就会被解压到指定容器文件系统的路径<dest>。
>- URL下载和解压特性不能一起使用。任何压缩文件通过URL拷贝，都不会自动解压。
>
>Copy :
>- 只复制文件 
>
>Dockerfile 里添加文件建议使用 Copy, 除非明确需要使用ADD.

运行 `docker build -t docker-ssh:v1 -f Dockerfile .` 构建镜像。
注意：`Forbidden path outside of the build context`错误，解决方案[参考](http://blog.csdn.net/zssureqh/article/details/52009043)

这样，基于python2.7的python开发镜像变做好了，自己需要什么python依赖直接写到requirements文件里即可。


### 第二步，启动容器，开发项目：django 项目为例

在目录`/Users/pylixm/docker.dev/django-demo/`下，运行`django-admin startproject mysite`在本地目录创建django项目, 目录如下：

```bash
$ tree
.
├── Dockerfile
├── manage.py
├── mysite
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── requirements.txt
```

运行一下命令以bash模式启动容器：
```
docker run -it --rm -p 80:80 -v /Users/pylixm/docker.dev/django-demo/mysite:/code/mysite docker-ssh:v1 bash
```
>说明：
>* -it：这是两个参数，一个是 -i：交互式操作，一个是 -t 终端。我们这里打算进入 bash 执行一些命令并查看返回结果，因此我们需要交互式终端。
>* --rm：这个参数是说容器退出后随之将其删除。默认情况下，为了排障需求，退出的容器并不会立即删除，除非手动 docker rm。我们这里只是随便执>行个命令，看看结果，不需要排障和保留结果，因此使用 --rm 可以避免浪费空间。
>* -p hostPort:containerPort : 映射容器端口到主机端口，前面是主机端口，后边是容器端口；
>* -v 主机目录:容器内目录 ：挂载主机目录作为容器的持久化数据卷。主机目录必须是`绝对路径`；
>* bash：放在镜像名后的是命令，这里我们希望有个交互式 Shell，因此用的是 bash。

此处利用容器的数据卷，将我们的开发项目映射到容器中，当我们的项目文件发生电话时会立即体现在容器中。容器关闭后，项目的变动任然存在。这样便可以愉快的使用docker来封装我们的开发环境了。

可进入容器，运行`python manage.py runserver 0.0.0.0:80`启动django项目。在我们主机的浏览器访问`0.0.0.0:80`, 便可看到项目页面了。

我们也可改造Dockerfile，设置暴露端口，和执行的命令,重新编译镜像。设置好后，我们便不用再进入容器启动运行django项目启动命令。
```
## 暴露docker容器的端口
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```
或者直接在`docker run ` 命令后加启动命令:
```
docker run -it --rm -p 80:8000 -v /Users/pylixm/docker.dev/django-demo/mysite:/code/mysite docker-ssh:v1 python ./mysite/manage.py runserver 0.0.0.0:8000
```


### 第三步，在pycharm中配置使用

第二步的时候，我们构建了我们的python开发镜像。我们只需要在pycharm中配置`Project Interpreter `即可。

**检查**
在Mac上开发，需要保证`Docker for Mac`启动，并配置好`Docker API`(Preferences | Build, Execution, Deployment | Docker)，如下图：
![](/static/imgs/docker-connect.png)

**配置**

- 1、到`Preferences -> Project Interpreter -> Add Romete `，选择本地的可用Docker 镜像,如图：
![](/static/imgs/docker-config-1.png)

- 2、配置`Edite configrations`, 将host设置为`0.0.0.0`, 选择刚才添加的项目解释器，并配置容器运行参数`Docker container settings`，如图：
![](/static/imgs/docker-config-2.png)

>说明：
>    - 容器端口：8000 映射到主机端口 80
>    - 挂载项目目录的数据卷： ` /Users/pylixm/docker.dev/django-demo/mysite:/code/mysite`

- 3、正常启动项目，访问`http://0.0.0.0:80`,即可看到亲切的欢迎界面。


更加详细配置说明参见[译 - 在pycharm中使用docker](http://pylixm.cc/posts/2017-10-29-Docker-use_in_pycharm.html)。

## Docker 其他知识点

### Docker for Mac 的安装路径
/Users/{YourUserName}/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/Docker.qcow2

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

## Docker 其他相关文档收集 

###  docker images 保存路径 及说明
http://blog.csdn.net/wanglei_storage/article/details/50299491

### docker 镜像与容器存储目录结构精讲 
http://blog.csdn.net/wanglei_storage/article/details/50299491



## 参考

- [http://blog.csdn.net/yhcvb/article/details/45696961](http://blog.csdn.net/yhcvb/article/details/45696961)
- [http://blog.csdn.net/wind_602/article/details/77988395](http://blog.csdn.net/wind_602/article/details/77988395)