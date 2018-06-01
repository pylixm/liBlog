---
layout : post
title : mongodb 启动报错
category : mongodb
date : 2016-04-06 
tags : [mongodb, 启动报错]
---


### Q & A：

错误信息：

    [root@localhost master]# mongod -f master.conf
    about to fork child process, waiting until server is ready for connections.
    forked process: 6040
    ERROR: child process failed, exited with error number 100

日志信息：

    2016-04-06T09:37:19.411+0200 I CONTROL  [main] ***** SERVER RESTARTED *****
    2016-04-06T09:37:19.421+0200 I CONTROL  [initandlisten] MongoDB starting : pid=5281 port=27017 dbpath=/var/lib/mongo 64-bit host=localhost
    2016-04-06T09:37:19.421+0200 I CONTROL  [initandlisten] db version v3.2.4
    2016-04-06T09:37:19.421+0200 I CONTROL  [initandlisten] git version: e2ee9ffcf9f5a94fad76802e28cc978718bb7a30
    2016-04-06T09:37:19.421+0200 I CONTROL  [initandlisten] OpenSSL version: OpenSSL 1.0.1e-fips 11 Feb 2013
    2016-04-06T09:37:19.421+0200 I CONTROL  [initandlisten] allocator: tcmalloc
    2016-04-06T09:37:19.421+0200 I CONTROL  [initandlisten] modules: none
    2016-04-06T09:37:19.421+0200 I CONTROL  [initandlisten] build environment:
    2016-04-06T09:37:19.421+0200 I CONTROL  [initandlisten]     distmod: rhel62
    2016-04-06T09:37:19.421+0200 I CONTROL  [initandlisten]     distarch: x86_64
    2016-04-06T09:37:19.421+0200 I CONTROL  [initandlisten]     target_arch: x86_64
    2016-04-06T09:37:19.421+0200 I CONTROL  [initandlisten] options: { config: "/etc/mongod.conf", net: { bindIp: "127.0.0.1", port: 27017 }, processManagement: { fork: true, pidFilePath: "/var/run/mongodb/mongod.pid" }, storage: { dbPath: "/var/lib/mongo", journal: { enabled: true } }, systemLog: { destination: "file", logAppend: true, path: "/var/log/mongodb/mongod.log" } }
    2016-04-06T09:37:19.448+0200 E NETWORK  [initandlisten] Failed to unlink socket file /tmp/mongodb-27017.sock errno:1 Operation not permitted
    2016-04-06T09:37:19.448+0200 I -        [initandlisten] Fatal Assertion 28578
    2016-04-06T09:37:19.449+0200 I -        [initandlisten]

### 原因：

上次mongodb没有正常启动或关闭。


### 解决方案：

直接删除 ``/tmp/mongodb-27017.sock `` 锁文件即可。
