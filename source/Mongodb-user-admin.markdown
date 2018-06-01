---
layout : post
title : mongodb 3.2 用户权限管理配置
category : mongodb
date : 2016-06-03
tags : [mongodb,]
---

使用mongodb 有段时间了，由于是在内网使用，便没有设置权限，一直是裸奔。

最近有时间，研究了下mongodb 3.2 的用户权限配置，网上有许多用户权限配置的文章，不过大多是之前版本，有些出入，特记录备查。

## 环境 

MongoDB shell version: 3.2.6

CentOS release 6.8 (Final)

## 设置方法

### 用户权限设置

- 1、进入mongodb的shell ： `mongo`

- 2、切换数据库： `use admin`

从3.0 版本起，默认只有 `local` 库，没有`admin` 库，需要我们自己来创建。

- 3、添加用户，指定用户的角色和数据库：

```bash
db.createUser(  
  { user: "admin",  
    customData：{description:"superuser"},
    pwd: "admin",  
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]  
  }  
)  

user字段，为新用户的名字；

pwd字段，用户的密码；

cusomData字段，为任意内容，例如可以为用户全名介绍；

roles字段，指定用户的角色，可以用一个空数组给新用户设定空角色。在roles字段,可以指定内置角色和用户定义的角色。
```

- 4、查看创建的用户 ： `show users` 或 `db.system.users.find()`

- 5、启用用户权限：

修改配置文件，增加配置：

```mongo
security:
  authorization: enabled

```

重新启动mongodb， `/etc/init.d/mongod restart`

- 6、用户验证使用：

启用用户验证后，再次登录mongo shell ，执行 `show dbs` 等命令会提示“没有权限”。此时，需要用户验证登录。

```bash
db.auth("admin","admin")  
```


### 其他

#### 内建的角色

1. 数据库用户角色：read、readWrite;
2. 数据库管理角色：dbAdmin、dbOwner、userAdmin；
3. 集群管理角色：clusterAdmin、clusterManager、clusterMonitor、hostManager；
4. 备份恢复角色：backup、restore；
5. 所有数据库角色：readAnyDatabase、readWriteAnyDatabase、userAdminAnyDatabase、dbAdminAnyDatabase
6. 超级用户角色：root  
// 这里还有几个角色间接或直接提供了系统超级用户的访问（dbOwner 、userAdmin、userAdminAnyDatabase）
7. 内部角色：__system

官方详情角色说明 --> [传送门](https://docs.mongodb.com/manual/reference/built-in-roles/#built-in-roles)


#### 配置文件示例 

官方详解 --> [传送门](https://docs.mongodb.com/manual/reference/configuration-options/)

```yaml
#此处为配置文件可配置的内容
#Mongod config file 
#MongoDB configuration files use the YAML format.
#The following example configuration file contains several mongod settings.
#
########Example Start########
#systemLog:
#   destination: file
#   path: "/var/log/mongodb/mongodb.log"
#   logAppend: true
#storage:
#   journal:
#      enabled: true
#processManagement:
#   fork: true
#net:
#   bindIp: 127.0.0.1
#   port: 27017
#setParameter:
#   enableLocalhostAuthBypass: false
#
########Example End########
#
########Core Options
systemLog:
#   verbosity: 0    #Default: 0; 1 to 5 increases the verbosity level to include Debug messages.
#   quiet: <boolean>
#   traceAllException: <boolean>
#   syslogFacility: user
   path: "/usr/local/mongodb/log/mongod.log"
   logAppend: true
#   logRotate: <string>    #rename or reopen
   destination: file
#   timeStampFormat: iso8601-local
#   component:
#      accessControl:
#         verbosity: 0
#      command:
#         verbosity: 0
#      # COMMENT additional component verbosity settings omitted for brevity
#      storage:
#         verbosity: 0
#         journal:
#            verbosity: <int>
#      write:
#         verbosity: 0
#
#
########ProcessManagement Options
processManagement:
   fork: true
   pidFilePath: "/usr/local/mongodb/log/mongod.pid"
#
#
#########Net Options
net:
   port: 27017
#   bindIp: <string>    #Default All interfaces.
#   maxIncomingConnections: 65536
#   wireObjectCheck: true
#   ipv6: false
#   unixDomainSocket:
#      enabled: true
#      pathPrefix: "/tmp"
#      filePermissions: 0700
#   http:
#      enabled: false
#      JSONPEnabled: false
#      RESTInterfaceEnabled: false
#   ssl:
#      sslOnNormalPorts: <boolean>  # deprecated since 2.6
#      mode: <string>
#      PEMKeyFile: <string>
#      PEMKeyPassword: <string>
#      clusterFile: <string>
#      clusterPassword: <string>
#      CAFile: <string>
#      CRLFile: <string>
#      allowConnectionsWithoutCertificates: <boolean>
#      allowInvalidCertificates: <boolean>
#      allowInvalidHostnames: false
#      FIPSMode: <boolean>
#
#
########security Options
#security:
#   keyFile: <string>
#   clusterAuthMode: keyFile
#   authorization: disable
#   javascriptEnabled:  true
########security.sasl Options
#   sasl:
#      hostName: <string>
#      serviceName: <string>
#      saslauthdSocketPath: <string>
#
#
#########setParameter Option
setParameter:
   enableLocalhostAuthBypass: false
#   <parameter1>: <value1>
#   <parameter2>: <value2>
#
#
#########storage Options
storage:
   dbPath: "/data/db"
#   indexBuildRetry: true
#   repairPath: "/data/db/_tmp"
#   journal:
#      enabled: true
#   directoryPerDB: false
#   syncPeriodSecs: 60
   engine: "mmapv1"  #Valid options include mmapv1 and wiredTiger.
#########storage.mmapv1 Options
#   mmapv1:
#      preallocDataFiles: true
#      nsSize: 16
#      quota:
#         enforced: false
#         maxFilesPerDB: 8
#      smallFiles: false
#      journal:
#         debugFlags: <int>
#         commitIntervalMs: 100   # 100 or 30
#########storage.wiredTiger Options
#   wiredTiger:
#      engineConfig:
#         cacheSizeGB: <number>  #Default: the maximum of half of physical RAM or 1 gigabyte
#         statisticsLogDelaySecs: 0
#         journalCompressor: "snappy"
#         directoryForIndexes: false
#      collectionConfig:
#         blockCompressor: "snappy"
#      indexConfig:
#         prefixCompression: true
#
#
##########operationProfiling Options
#operationProfiling:
#   slowOpThresholdMs: 100
#   mode: "off"
#
#
##########replication Options
#replication:
#   oplogSizeMB: <int>
#   replSetName: <string>
#   secondaryIndexPrefetch: all
#
#
##########sharding Options
#sharding:
#   clusterRole: <string>    #configsvr or shardsvr
#   archiveMovedChunks: True
#
#
#########auditLog Options
#auditLog:
#   destination: <string>   #syslog/console/file
#   format: <string>   #JSON/BSON
#   path: <string>
#   filter: <string>
#
#
#########snmp Options
#snmp:
#   subagent: <boolean>
#   master: <boolean>
#
#
########mongos-only Options
#replication:
#   localPingThresholdMs: 15
#
#sharding:
#   autoSplit: true
#   configDB: <string>
#   chunkSize: 64
#
#
########Windows Service Options
#processManagement:
#   windowsService:
#      serviceName: <string>
#      displayName: <string>
#      description: <string>
#      serviceUser: <string>
#      servicePassword: <string>
```



---

## 参考：

- [http://bbs.51cto.com/thread-1164186-1-1.html](http://bbs.51cto.com/thread-1164186-1-1.html)
- [http://bbs.51cto.com/thread-1146654-1.html](http://bbs.51cto.com/thread-1146654-1.html)
- [http://blog.csdn.net/lk10207160511/article/details/50281883](http://blog.csdn.net/lk10207160511/article/details/50281883)

