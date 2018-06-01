---
layout : post
title : postgreSQL vs MySQL 命令行对比
category : postgreSQL
date : 2017-11-05
tags : [postgreSQL, mysql, 数据库]
---

>原文：http://www.cnblogs.com/qiyebao/p/4749146.html

## 服务启动
**PostgreSQL**
- 1)#service postgresql start
- 2)#/etc/init.d/postgresql start
- 3)#su – postgresql
- $pg_ctl start

**MySQL**
- 1)#service mysqld start
- 2)#/etc/init.d/mysqld start
- 3)#safe_mysqld&


## 第一次进入数据库
**PostgreSQL**
```bash
\#su – postgres
$createdb （建名为postgres的数据库）
$psql
```

**MySQL**
```bash
\#mysql
mysql> (出现这个提示符说明成功)
```


## 创建用户：(用户Ajian，密码：123)
**PostgreSQL**
```bash
#su – postgres
$psql
=#create user ajian with password ‘123’;
```

**MySQL**
```sql
#grant all privileges on *.* to ajian@”%” identified by “123″
-- (注意：同还可以分配权限，这里是ALL)
``` 


## 创建数据库
**PostgreSQL**
```bash 
#su – postgres
$psql
=#create database My with owner = ajian template = template1 encoding=’UNICODE’;
```

**MySQL**
```bash 
1)#mysql
Mysql>create database My;
2)#mysqladmin create My
```


## 查看用户和数据库
**PostgreSQL**
```bash 
#su – postgres
$psql
=#\l (查看数据库)
=#\du (查看用户)
=#\c 从一个数据库中转到另一个数据库中，如template1=# \c sales 从template1转到sales
```

**MySQL**
```
1)#mysql
Mysql>show databases; (看数据库)
2)#mysqlshow
use dbname;
```

## 新建用户登录
**PostgreSQL**
1、首先修改配置文件
# vi /var/lib/pgsql/data/pg_hba.conf(在最后加)

host all all 127.0.0.1 255.255.255.255 md5

2、再重启服务：
#service postgresql restart

3、登录：#psql –h 127.0.0.1 –U ajian My

Password:
```

**MySQL**
```bash 
1)#mysql –u ajian –p (带口令登录)

2)#mysql

Mysql>use My;

(不带口令登录一般用于本机)
```

## 创建表(employee)
**PostgreSQL**
```bash 
=#create table employee(

(#employee_id int primary key,

(#name char(8),

(#sex char(2));
```

**MySQL**
```bash 
>create table employee(

->employee_id int primary key,

->name char(8),

->sex char(2));
```

## 查看表
**PostgreSQL**
```
=#\dt
```

**MySQL**
```
>show tables;
```

## 查看表的结构：
**PostgreSQL**
```
=#\d employee
```

**MySQL**
```
>sescribe employee;
``` 

## 向表中添加数据：
**PostgreSQL**
```
=#insert into employee values

-#(‘1’,’zhang’,’F’);

-#(‘2’,’chen’,’M’,);
```

**MySQL**
```
>insert into employee values

->(‘1’,’zhang’,’F’);

->(‘2’,’chen’,’M’,);
```

## 查看表的数据
**PostgreSQL**
```
=#select * from emlpoyee
```

**MySQL**
```
>select * from emlpoyee;
```

## 索引相关

**PostgreSQL**
```bash 
## 创建索引(IN_employee)
=#create index IN_employee on employee(name);
## 查看索引
=#\di
## 删除索引
=#drop index IN_employee on employee;
## 重建索引
=#reindex table employee;(重建employee所有的)

=#reindex index IN_employee;(重建指定的)
```

**MySQL**
```bash 
## 创建索引(IN_employee)

1)>create index IN_employee on employee(name);

2)>alter table employee add index IN_employee(name);

## 查看索引：

>show index from employee;

## 删除索引：

1)>drop index IN_employee on employee;

2)>alter table emlpoyee drop index IN_employee;
```

## 删除表
**PostgreSQL**
```bash 
=#drop table employee;
```

**MySQL**
```bash 
>drop table employee;
```

## 删除数据库：(注意命令前面的标志)
**PostgreSQL**
```
1)=#drop database ajian;

2)$dropdb ajian
```
**MySQL**
```
1）>drop database ajian;

2)#mysqladmin drop ajian
```
