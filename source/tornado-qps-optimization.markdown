---
layout : post
title : 记一次tornado QPS 优化
category : tornado
date : 2017-04-04 20:00:00
tags : [tornado]
---

应项目的需求，我们使用tornado开发了一个api系统，系统开发完后，在8核16G的虚机上经过压测qps只有200+。与我们当初定的QPS 大于2k差了一个数量级，于是便开始了漫长的优化之路。在优化过程中，学了许多东西，有必要整理记录下备查。

我们的技术选型：
- python2.7
- tornado4.4.3
- sqlalchemy1.1.5
- mysql5.6
- rabbitmq

当初技术选型的时候选择tornado，便是因为其优秀的性能，这么低的QPS自然是不甘心。究竟tornado可以达到多少QPS呢？于是编写了简单的hello world,在上边的虚拟机中起16个进程下，使用ab压测QPS竟然达到了惊人的6K，平均响应时间在毫秒级。这下有信心将api的QPS继续优化了。
<!-- more -->
## 初步分析

提升QPS, 可从两方面入手，一个是增加并发数，其二是减少平均响应时间。从目前情况看，增加进程并发数是最直接的手段，但当达到机器资源的瓶颈时，可靠堆叠机器来解决。那么
相比较下，减小平均响应更为重要。初步分析了我们开发的api，平均响应时间在几百毫秒级别。大部分的时间花在系统与数据库的交互上，到这，便有了一个优化的主题思路：最大限度的降低平均响应时间。

我们API完成的功能为，接受请求参数做一些列的认证判断（与数据库交互），将消息以广播的形式发送到rabbitmq供消费者消费,最后返回给客户端发送结果。根据此逻辑，影响响应时间的地方，分析如下：

- 与mysql 数据库的交互
- 使用rabbitmq广播消息时的时间耗费
- 耗时的业务逻辑代码片段

## 优化思路

根据上边的问题，从以下几个方面入手：

- 增加tornado的异步特性
- 分析与数据库的交互，减少与数据库的交互时间
- 分析rabbitmq的时间耗费，减少发送信息时间
- 优化业务代码逻辑

## 具体实施

### tornado 的异步特性

开发api时，因为对tornado 的异步特性不是很熟悉，便没有使用。后来随着测试的深入，发现需要使用后，开始了解。
随着了解的深入，发现tornado是并没有很好的支持数据库的异步特性，更多是对网络的异步，官网上也是写的”网络非阻塞框架“。
查阅官方文档，tornado的异步实现，见[官方文档](http://www.tornadoweb.org/en/stable/guide/async.html)
总的来说，使程序异步的方式有3种，参考[这里](https://juejin.im/post/588e0de45c497d0056cadcbf)。如下：
- 第一种，使用tornado 的 gen.coruntine。
    使用此种方式，需要异步数据库的驱动库，经查找现阶段并没有很好的成熟的支持异步查询mysql的python驱动，放弃此种方案。
- 第二种，使用tornado 的线程模块。
    此种方式比较方便，只需要在耗时的函数上添加装饰器即可，简单方便，可以说是一种万能方案，但此方案耗费系统资源。
    系统资源并不是我们的瓶颈，我们最后采纳了此种方式。
- 第三种，使用外部队列，单独其worker 进程或线程去处理。例如，celery 等。
    此种方式增加了外部的依赖，增加了系统的复杂性和后期的维护难度，放弃此种方案。

增加了异步特性外有显著的提升。

### mysql 数据库的优化

数据库方便，我们适用的是SQLAlchemy。使用ORM时，在减少裸sql带来的查询复杂度的同时，必然会增加查询数据库的耗时。我们也做过测试，
使用pymsql链接mysql,直接使用裸sql查询与使用sqlalcemy 的对象查询的耗时差别有7、8个毫秒的时差，与sqlalchemy的裸sql方式执行时间几乎一致。
可见，sqlalchemy的orm方式是有一定时间耗损的。stackoverflow的一个问题，也验证了我的想法，见[Why is loading SQLAlchemy objects via the ORM 5-8x slower than rows via a raw MySQLdb cursor?](http://stackoverflow.com/questions/23185319/why-is-loading-sqlalchemy-objects-via-the-orm-5-8x-slower-than-rows-via-a-raw-my)

针对数据库方面，我们做了如下优化：
- 将SQLAlchemy 查询改为核心裸sql方式，可参考[这里](http://docs.sqlalchemy.org/en/latest/faq/performance.html#result-fetching-slowness-orm)。
- 优化数据库，增加必要的索引。
- 将逻辑中的过滤条件，尽量的移到sql中，减少sql结果集的大小，加快查询速度。
- 将可以单词查询出的数据集放到一次查询中，减少链接数据库的次数。


### 分析rabbitmq的时间耗费，减少发送信息时间

rabbitmq 方面，使用的是[pika](https://pika.readthedocs.io/en/0.10.0/) 作为驱动库连接的，使用方式是每次发送数据的时候创建链接和通道，发送完毕后立即关闭链接。考虑到是否可以使用长链接，创建链接后不关闭，只关闭channel。修改后发现报错,具体代码如下：

```python
# -*- coding:utf-8 -*-
import pika
from settings import settings


class Client(object):
    def __init__(self, host, port, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.init_connection()

    def init_connection(self):
        user_pwd = pika.PlainCredentials(self.username, self.pwd)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=user_pwd))

    # ... 
```
>补充错误材料分析 - todo

翻阅了pika的文档，发现其有异步的使用方式，且有与tornando 框架的结合的实例，见[文档](https://pika.readthedocs.io/en/0.10.0/examples/asynchronous_publisher_example.html)。
pika的异步方式，使用了和tornado 相同的基于epull的事件循环模型，如何将其与tornado 的IOloop结合是个问题，
其有个tornado的链接适配器，翻看其代码还是有些不太明确如何使用，有时间的时候再继续研究下。

针对rabbitmq的优化我们放弃了，但优化过程中有些值得分析的文章，整理如下：
- [rabbitmq-amqp-channel-best-practices](https://www.oschina.net/translate/rabbitmq-amqp-channel-best-practices)
- [rabbitmq-best-practices-for-designing-exchanges-queues-and-bindings](https://derickbailey.com/2015/09/02/rabbitmq-best-practices-for-designing-exchanges-queues-and-bindings/)
- [tornado与pika结合实例](https://reminiscential.wordpress.com/2012/04/07/realtime-notification-delivery-using-rabbitmq-tornado-and-websocket/)


### 优化业务代码逻辑

代码逻辑方便的优化，如下：
- 减少循环
- review 逻辑，去除冗余逻辑
- 提去公共变量，赋值一次，减少查询数据库。


## 总结

经过以上的优化，我们的api 的 QPS 提升到了1200+, 由于时间问题，我们暂停了继续的优化。通过本次QPS的优化过程，有几点感悟：
- 使用一项新技术时，一定要认真阅读官方文档，了解清楚后，再使用。
- 不要轻易否定一项公认的“技术真理”，要拿数据说话。


## 个人工作总结，欢迎留言交流！

