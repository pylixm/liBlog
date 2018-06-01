---
layout : post
title : Docker学习笔记--网络配置
category : docker
date : 2018-05-24
tags : [devops, 自动化运维, docker]
---

## Linux 的虚拟化技术

## Docker的网络配置

### 从容器内访问宿主机服务

当容器访问本地的数据库时，可使用如下地址：

**MacOS with earlier versions of Docker**
- Docker v 18.03 and above (since March 21st 2018)
Use your internal IP address or connect to the special DNS name `host.docker.internal` which will resolve to the internal IP address used by the host.
- Docker for Mac v 17.12 to v 18.02
Same as above but use `docker.for.mac.host.internal` instead.
- Docker for Mac v 17.06 to v 17.11
Same as above but use `docker.for.mac.localhost` instead.
- Docker for Mac 17.05 and below
To access host machine from the docker container you must attach an IP alias to your network interface. You can bind whichever IP you want, just make sure you're not using it to anything else.
`sudo ifconfig lo0 alias 123.123.123.123/24`

**Linux **
- docker run --net="bridge" (default): 使用 docker0 的ip地址。


## 参考
- [Linux上虚拟网络与真实网络的映射](https://www.sdnlab.com/13539.html)
- [Linux-虚拟网络设备-veth pair](https://blog.csdn.net/sld880311/article/details/77650937)
- [Linux 中的虚拟网络](https://www.ibm.com/developerworks/cn/linux/l-virtual-networking/)
- [from-inside-of-a-docker-container-how-do-i-connect-to-the-localhost-of-the-mach](https://stackoverflow.com/questions/24319662/from-inside-of-a-docker-container-how-do-i-connect-to-the-localhost-of-the-mach/24326540#24326540)


http://dockone.io/article/1261
https://blog.csdn.net/huanongying123/article/details/73556634
https://blog.csdn.net/u010884123/article/details/55213190