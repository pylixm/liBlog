---
layout : post
title : rabbitmq 安装配置记录
category : rabbitmq
date : 2016-01-19
tags : [rabbitmq,]
---



最近做系统迁移，搭建环境时遇到了rabbitmq的搭建。在此记录，备查。

环境：

- centos 6.5 

官方centos安装文档：[http://www.rabbitmq.com/install-rpm.html](http://www.rabbitmq.com/install-rpm.html)

其他系统安装文档：[http://www.rabbitmq.com/download.html](http://www.rabbitmq.com/download.html)
<!-- more -->
### 0x00 安装Erlang

因为rabbitmq依赖Erlang，安装前需要先安装Erlang。

    yum install erlang
    
### 0x01 安装rabbitmq

    rpm --import https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
    yum install rabbitmq-server-3.6.0-1.noarch.rpm
    
    注：使用yum 安装时，遇到问题没有安装包的错误。把版本号去掉，即可正常安装。
    
### 0x02 启动rabbitmq

    service rabbitmq-server stop/start/restart
    /etc/init.d/rabbitmq-server stop/start/restart
    # 开机启动
    chkconfig rabbitmq-server on
    
### 0x03 链接端口

    4369 (epmd), 25672 (Erlang distribution)
    5672, 5671 (AMQP 0-9-1 without and with TLS)
    15672 (if management plugin is enabled)
    61613, 61614 (if STOMP is enabled)
    1883, 8883 (if MQTT is enabled)
    
### 0x04 安装 RabbitMQ Web管理插件

在终端执行如下命令即安装成功：

    rabbitmq-plugins enable rabbitmq_management  
    service rabbitmq-server restart  
 
打开浏览器登录：http://127.0.0.1:15672  55672也可以，直接跳转到下列web管理
登录 账号密码默认都是 guest

### 0x05 rabbitmq 相关管理命令

1、virtual_host管理

      新建virtual_host: rabbitmqctl add_vhost  xxx
      撤销virtual_host: rabbitmqctl delete_vhost xxx
      
2、用户管理

      新建用户：rabbitmqctl add_user xxxpwd
      删除用户: rabbitmqctl delete_user xxx
      改密码: rabbimqctl change_password {username} {newpassword}
      设置用户角色：rabbitmqctl set_user_tags {username} {tag ...}
              Tag可以为 administrator, monitoring, management
3、权限管理
      权限设置：rabbitmqctl set_permissions [-pvhostpath] {user} {conf} {write} {read}
               Vhostpath
               Vhost路径
               user
      用户名
              Conf
      一个正则表达式match哪些配置资源能够被该用户访问。
              Write
      一个正则表达式match哪些配置资源能够被该用户读。
               Read
      一个正则表达式match哪些配置资源能够被该用户访问。
      
      赋予全部权限：
      
      rabbitmqctl set_permissions -p vir_host tonyg ".*" ".*" ".*"


更多管理命令见官网文档：[http://www.rabbitmq.com/man/rabbitmqctl.1.man.html#Access%20control](http://www.rabbitmq.com/man/rabbitmqctl.1.man.html#Access%20control)





### 参考

- [http://www.rabbitmq.com/install-rpm.html](http://www.rabbitmq.com/install-rpm.html)

- [http://blog.csdn.net/mlks_2008/article/details/18988301](http://blog.csdn.net/mlks_2008/article/details/18988301)

- [http://stackoverflow.com/questions/26624263/celery-didnt-operate-well-because-of-errno-104](http://stackoverflow.com/questions/26624263/celery-didnt-operate-well-because-of-errno-104)