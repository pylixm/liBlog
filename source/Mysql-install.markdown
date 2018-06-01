---
layout : post
title : Mysql 免安装版配置 window环境搭建
category : mysql
date : 2015-11-01
tags : [mysql]
---


1. 下载MySQL Community Server 5.6.13

2. 解压MySQL压缩包
    将以下载的MySQL压缩包解压到自定义目录下,我的解压目录是:
    "D:\Program Files\MySQL\mysql-5.6.13-win32"
    将解压目录下默认文件 my-default.ini 拷贝一份，改名 my.ini
    复制下面的配置信息到 my.ini 保存
    #如果没有my-default.ini,可自己新建my.ini或者从其他地方中获取
#########################################################
    [client]
    port=3306
    default-character-set=utf8
    [mysqld]
    port=3306
    character_set_server=utf8
    basedir=D:\Program Files\MySQL\mysql-5.6.13-win32
    #解压目录
    datadir=D:\Program Files\MySQL\mysql-5.6.13-win32\data
    #解压目录下data目录
    sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
    [WinMySQLAdmin]
    D:\Program Files\MySQL\mysql-5.6.13-win32\bin\mysqld.exe
#########################################################



3. 添加环境变量

    操作如下：
    1）右键单击我的电脑->属性->高级系统设置(高级)->环境变量
      点击系统变量下的新建按钮
      输入变量名：MYSQL_HOME
      输入变量值：D:\Program Files\mysql-5.6.11-winx64
      #即为mysql的自定义解压目录。
    2）选择系统变量中的Path
      点击编辑按钮
      在变量值中添加变量值：%MYSQL_HOME%\bin
      注意是在原有变量值后面加上这个变量，用;隔开，不能删除原来的变量值，



4. 将mysql注册为windows系统服务

    1）从控制台进入到MySQL解压目录下的 bin 目录下：
    2）输入服务安装命令：

    mysqld install MySQL --defaults-file="D:\Program Files\MySQL\mysql-5.6.13-win32\my.ini"

   注：

   a、该命令要在 %%/bin 目录下执行，否则报错：

     系统错误2：系统找不到指定的文件.

    出现这种错误的原因是在注册系统服务的时候 没有进入到 %mysql 的解压目%\bin 目录下， 即使配置了环境变量，也要进入该目录下进行注册 ，否     则注册的服务“可执行文件路径”会默认在 C 盘下。详见：http://blog.163.com/peijian1008%40126/blog/static/95311581201342710151205/）

    b、1067错误，造成此问题的原因众多，网络先人已有总结，见http://blog.csdn.net/love_baobao/article/details/6922939

   按以上命令执行后报错，问题如下：

    》 配置文件，注意源文件中的   [mysqld], 复制的时候不要与原文件重复

    》换命令执行“ mysqld --install  ” ，配置文件使用原配置文件（“my-default.ini”） 名称不要改。

  #解压目录下修改的my.ini文件

    安装成功后会提示服务安装成功。
    #注：my.ini文件放在MySQL解压后的根目录下
    #移除服务命令为：mysqld remove



5. 启动MySQL服务

    方法一：
        启动服务命令为：net start mysql
    方法二：
        打开管理工具 服务，找到MySQL服务。
        通过右键选择启动或者直接点击左边的启动来启动服务。



6. 修改 root 账号的密码

    刚安装完成时root账号默认密码为空，此时可以将密码修改为指定的密码。如：123456
    c:>mysql –uroot
    mysql>show databases;
    mysql>use mysql;
    mysql>UPDATE user SET password=PASSWORD("123456") WHERE user='root';
    mysql>FLUSH PRIVILEGES;
    mysql>QUIT

7. MySQL控制台快捷方式建立:
    1）桌面右键->新建->快捷方式->对象位置输入：C:\Windows\System32\cmd.exe
        快捷方式名称自己定义，确定，快捷方式建立成功
    2）右键单击刚才建立的快捷方式->属性->把目标一栏修改成MySQL启动参数：
        C:\Windows\System32\cmd.exe "D:\Program Files\MySQL\mysql-5.6.13-win32\bin" /k mysql -uroot -p inventory
        解释:CMD路径 "MySQL路径bin目录" /k mysql -u用户名 -p密码 数据库名

    3）修改完成后点击确定保存，直接双击快捷方式即可连接到MySQL数据库