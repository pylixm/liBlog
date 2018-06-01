---
layout : post
title : SaltStack学习笔记1-salt安装配置
category : salt
date : 2015-12-17 23:33:00
tags : [salt]
---


Salt，一种全新的基础设施管理方式，部署轻松，在几分钟内可运行起来，扩展性好，很容易管理上万台服务器，速度够快，服务器之间秒级通讯。

salt底层采用动态的连接总线, 使其可以用于编配, 远程执行, 配置管理等等。

官方文档：[https://docs.saltstack.com/en/latest/](https://docs.saltstack.com/en/latest/)

中文文档：[http://docs.saltstack.cn/zh_CN/latest/](http://docs.saltstack.cn/zh_CN/latest/)

中文社区：[http://www.saltstack.cn/](http://www.saltstack.cn/)

### 0x00 saltstack 安装

salt安装分为 master 安装和 minion 的安装。

centos6.6 为例(其他系统见官网：[这里](https://docs.saltstack.com/en/latest/topics/installation/index.html#platform-specific-installation-instructions))

#### 1、开启EPEL

EPER源(EPEL 是yum的一个软件源，里面包含了许多基本源里没有的软件。)

<del>rpm -Uvh http://ftp.linux.ncsu.edu/pub/epel/6/i386/epel-release-6-8.noarch.rpm </del>


20160303 update:

rpm --import https://repo.saltstack.com/yum/redhat/6/x86_64/latest/SALTSTACK-GPG-KEY.pub

设置yum 源  ``/etc/yum.repos.d/saltstack.repo``

    [saltstack-repo]
    name=SaltStack repo for RHEL/CentOS $releasever
    baseurl=https://repo.saltstack.com/yum/redhat/$releasever/$basearch/latest
    enabled=1
    gpgcheck=1
    gpgkey=https://repo.saltstack.com/yum/redhat/$releasever/$basearch/latest/SALTSTACK-GPG-KEY.pub

更新yum源 

sudo yum clean expire-cache.

sudo yum update.

#### 2、安装master和minion

Salt的master和minion包是分开的。机器只需要安装相应的包即可运行。通常情况下，会有一个master和多个minions

- 在salt-master上，运行:
    
    ``yum install salt-master``

- 在salt-minion上，运行:

    ``yum install salt-minion``

### 0x01 saltstack 配置

#### 1. master配置

配置文件 `/etc/salt/master` ，master的相关配置在此修改，配置如下。

`insterface: 192.168.33.10` 绑定master的通信 IP

#### 2. minion配置

配置文件 `/etc/salt/minion` ，minion的配置文件位置同master。minion安装后需要修改配置如下：

`master: 192.168.33.10` # 指定master的地址

#### 3. master与minion认证

- 启动master 

`/etc/init.d/salt-master start`

- 启动minion 

`/etc/init.d/salt-minion start`

- 当minion启动时，会向配置文件中配置的master发送自己的key，作为认证实用。key的取值，默认取第一个网卡的ip作为key。也可以在minion配置文件中，配置`id: minion的key `

- 在master 执行 `salt-key -L` 查看链接此master的所有minion的key。执行 `salt-key -a minion的key` 来添加minion的认证。

- 执行 `salt 192.168.33.11 test.ping` 来测试minion的连通性。

```bash 

[root@localhost salt]# salt-key -L
Accepted Keys:
Denied Keys:
Unaccepted Keys:
192.168.33.11
Rejected Keys:
[root@localhost salt]# salt-key -a 192.168.33.11
The following keys are going to be accepted:
Unaccepted Keys:
192.168.33.11
Proceed? [n/Y] y
Key for minion 192.168.33.11 accepted.
[root@localhost salt]# salt-key -L
Accepted Keys:
192.168.33.11
Denied Keys:
Unaccepted Keys:
Rejected Keys:
[root@localhost salt]# salt '192.168.33.11' test.ping 
192.168.33.11:
    True

```

#### 4.其他

1、默认的日志路径： /var/log/salt

2、有时使用``test.ping`` 测试minion不通。很大可能是因为认证的问题，注意salt 的认证机制。

- 启动master， master 会生成秘钥保存在 ``pki`` 目录中。

- 启动minion， minion 会生成秘钥也保存在 pki 目录中。

- master 通过保存在pki中的秘钥做相关认证。

所以，当秘钥发声变化的时候就ping 不通了。此时，可以尝试删除 pki 目录，重启重新认证。







### salt 博客推荐

在学习salt时，收集到的比较靠谱的博客：

[小马的博客salt系列](http://www.xiaomastack.com/category/salt/)

[灿哥的Blog](http://www.shencan.net/index.php/category/%E8%87%AA%E5%8A%A8%E5%8C%96%E8%BF%90%E7%BB%B4/saltstack/)

### 参考：

[https://docs.saltstack.com/en/latest/](https://docs.saltstack.com/en/latest/)