---
layout : post
title : 转载-Memcached, Redis, MongoDB区别
category : NoSQL
date : 2015-11-30 22:22:00
tags : [NoSQL, redis]
old_url : http://www.cnblogs.com/davidgu/p/3665589.html
---


mongodb和memcached不是一个范畴内的东西。mongodb是文档型的非关系型数据库，其优势在于查询功能比较强大，能存储海量数据。mongodb和memcached不存在谁替换谁的问题。

和memcached更为接近的是redis。它们都是内存型数据库，数据保存在内存中，通过tcp直接存取，优势是速度快，并发高，缺点是数据类型有限，查询功能不强，一般用作缓存。在我们团队的项目中，一开始用的是memcached，后来用redis替代。

相比memcached：

1、redis具有持久化机制，可以定期将内存中的数据持久化到硬盘上。

2、redis具备binlog功能，可以将所有操作写入日志，当redis出现故障，可依照binlog进行数据恢复。

3、redis支持virtual memory，可以限定内存使用大小，当数据超过阈值，则通过类似LRU的算法把内存中的最不常用数据保存到硬盘的页面文件中。

4、redis原生支持的数据类型更多，使用的想象空间更大。

5、前面有位朋友所提及的一致性哈希，用在redis的sharding中，一般是在负载非常高需要水平扩展时使用。我们还没有用到这方面的功能，一般的项目，单机足够支撑并发了。redis 3.0将推出cluster，功能更加强大。

6、redis更多优点，请移步官方网站查询。

7、 性能

Redis作者的说法是平均到单个核上的性能，在单条数据不大的情况下Redis更好。为什么这么说呢，理由就是Redis是单线程运行的。
因为是单线程运行，所以和Memcached的多线程相比，整体性能肯定会偏低。
因为是单线程运行，所以IO是串行化的，网络IO和内存IO，因此当单条数据太大时，由于需要等待一个命令的所有IO完成才能进行后续的命令，所以性能会受影响


* 原文地址：[http://www.cnblogs.com/davidgu/p/3665589.html](http://www.cnblogs.com/davidgu/p/3665589.html)