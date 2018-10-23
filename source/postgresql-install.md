---
layout : post
title : centos 7 下 postgreSQL 10 安装记录
category : postgreSQL
date : 2017-11-05
tags : [postgreSQL, 数据库]
---


最近工作中与数据库打交道越来越多，操作数据频繁，感觉到了许多mysql操作的不便利性。想起了几年前使用的 `postgreSQL`, 重新整理安装下，记录备查。

关于`mysql`和 `postgreSQL` 的对比可见知乎的这个问题[PostgreSQL 与 MySQL 相比，优势何在？](https://www.zhihu.com/question/20010554)。

看了下postgreSQL的发行版本，除了核心版本外还有针对大数据分析和虚拟化技术的分支版本，发展紧跟时代步伐，详见官方[这里](https://www.postgresql.org/download/)。对于postgreSQL的安装官方提供了许多方法，支持yum 安装、rpm安装、源码编译安装等方式。我这里采用yum 源安装，其他方式可参考[官方文档](https://www.postgresql.org/download/linux/redhat/)。安装步骤如下：
<!-- more -->
## 准备 

检查系统是否安装了postgresSQL。若安装了需要卸载，清理干净，防止造成安装时不必要的问题。
```bash 
# 检查是否安装 
rpm -qa | grep postgres    # 检查PostgreSQL 是否已经安装
rpm -qal | grep postgres   # 检查PostgreSQL 安装位置

# 卸载 
rpm -e postgresql94-contrib-9.4.4-1PGDG.rhel6.x86_64 postgresql94-server-9.4.4-1PGDG.rhel6.x86_64  
rpm -e postgresql94-libs-9.4.4-1PGDG.rhel6.x86_64 postgresql94-9.4.4-1PGDG.rhel6.x86_64 
```

## 安装yum 源 

在官方文档选择自己系统对应的参数，获取到yum源的正确连接，执行安装。
```bash 
yum install https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-1.noarch.rpm
```

## 安装客户端和服务端 

```bash 
yum install postgresql10
yum install postgresql10-server
```

## 初始化数据库，启动服务

```bash 
/usr/pgsql-10/bin/postgresql-10-setup initdb
systemctl enable postgresql-10
systemctl start postgresql-10
```

**说明：**
- 1、数据库默认路径：`/var/lib/pgsql/10/data` ;
- 2、修改默认初始化路径，使用`postgreSQL`自带的初始化命令`initdb`，如下操作：
```
#mkdir /opt/PostgreSQL
#mkdir /opt/PostgreSQL/data
#chmod 755 /opt/PostgreSQL/data
#chown postgres:postgres /opt/PostgreSQL/data
#su - postgres
#./initdb --encoding=UTF-8  --local=zh_CN.UTF8 --username=postgres --pwprompt --pgdata=/opt/PostgreSQL/data/
```


## 连接数据库

postgresql10 在Linux的安装，默认创建了`postgres`用户，无需再次创建，直接su 即可。
```bash 
[root@pylixm-web ~]# su - postgres
bash-4.2$ psql
psql (10.0)
Type "help" for help.

postgres=# \l
                                  List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-----------+----------+----------+-------------+-------------+-----------------------
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
(3 rows)

postgres=# \du
                                   List of roles
 Role name |                         Attributes                         | Member of
-----------+------------------------------------------------------------+-----------
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

postgres=#

```

## 数据库登录权限设置

`/var/lib/pgsql/10/data/pg_hba.conf` 权限相关配置:
```conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only 
local   all             all                                     peer 或 trust
# IPv4 local connections:
#host    all             all             127.0.0.1/32            ident
host    all             all             0.0.0.0/0               password
# IPv6 local connections:
#host    all             all             ::1/128                 ident
host    all             all             ::1/128                 password
# Allow replication connections from localhost, by a user with the
# replication privilege.
#local   replication     all                                     peer
#host    replication     all             127.0.0.1/32            ident
#host    replication     all             ::1/128                 ident
```
**说明：** 设置 trust，本地可以使用psql -U postgres直接登录服务器；设置 peer，本地可以使用psql -h 127.0.0.1 -d postgres -U postgres直接登录服务器; password ，使用用户名密码 登录 ；

`/var/lib/pgsql/10/data/postgresql.conf` 数据库相关配置:
```
listen_addresses = '*'
posrt = 5432 
```
**说明：** 监听任意IP, 允许任意ip连接数据库。

更多权限说明，见[官方文档](https://www.postgresql.org/docs/10/static/auth-methods.html)。

## 防火墙设置

此时，数据库可以在本地访问，要想在外部访问，还需要增加防火墙策略或直接关闭防火墙（不建议）。

centos 7 默认防火墙为 [`firewalld`](http://blog.csdn.net/gg_18826075157/article/details/72834694), 我们改用熟悉的`iptables`操作如下：
1、关闭firewall：
systemctl stop firewalld.service #停止firewall
systemctl disable firewalld.service #禁止firewall开机启动
firewall-cmd --state #查看默认防火墙状态（关闭后显示notrunning，开启后显示running）

2、iptables防火墙

`yum install iptables iptables-services`  ## 安装

`vim /etc/sysconfig/iptables `#编辑防火墙配置文件

```
# sampleconfiguration for iptables service
# you can edit thismanually or use system-config-firewall
# please do not askus to add additional ports/services to this default configuration
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT[0:0]
:OUTPUT ACCEPT[0:0]
-A INPUT -m state--state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p icmp -jACCEPT
-A INPUT -i lo -jACCEPT
-A INPUT -p tcp -mstate --state NEW -m tcp --dport 22 -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -jACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 5432-j ACCEPT
-A INPUT -j REJECT--reject-with icmp-host-prohibited
-A FORWARD -jREJECT --reject-with icmp-host-prohibited
COMMIT
:wq! #保存退出
```
`systemctl restart iptables.service` #最后重启防火墙使配置生效
`systemctl enable iptables.service` #设置防火墙开机启动

**注：** 若你使用的服务器为公有云产品，以上防火墙配置可能无限，有些公有云在控制台的安全组设置端口策略，如阿里云产品。

致此，我们已经安装并配置好数据库了，可以开心的使用了。更多进阶，可参考德哥文章[PostgreSQL 10.0 解读](https://yq.aliyun.com/articles/79330)

## 参考

- [http://www.cnblogs.com/qiyebao/p/4562557.html](http://www.cnblogs.com/qiyebao/p/4562557.html)
- [http://www.linuxidc.com/Linux/2015-05/117473.htm](http://www.linuxidc.com/Linux/2015-05/117473.htm)
- [https://my.oschina.net/myaniu/blog/181543](https://my.oschina.net/myaniu/blog/181543)