---
layout : post
title : 转-【SaltStack源码分析任】务处理机制
category : salt
date : 2017-09-01
tags : [salt, 源码分析]
---

> 原文地址：[http://jackywu.github.io/articles/saltstack%E6%BA%90%E7%A0%81%E5%88%86%E6%9E%90/](http://jackywu.github.io/articles/saltstack%E6%BA%90%E7%A0%81%E5%88%86%E6%9E%90/)

# 1. 前言

1. 本代码分析基于 saltstack－2015.8 版本
2. saltstack中大量使用了ZeroMQ，所以需要预先储备 [ZeroMQ方面的知识](http://zguide.zeromq.org/page:all)
3. 本文以运行 `salt '*' test.ping` 场景为例研究任务的处理机制。

# 2. 概念解释

Salt Client

> 运行在Salt Master上，给Master发送请求，并且得到结果返回的LocalClient类。

Salt Master有几个重要的类

1. Publisher：给Minion发送指令
2. EventPublisher：Master上的事件发布总线
3. MWorkers：Salt Master的工作进程
4. ReqServer：实现了一个MWorkers的多进程模型。接收Salt Client的请求或者Minion返回的结果，发送给MWorker去处理

# 3. 任务处理机制

1. 在Master上运行`salt '*' test.ping`, 原理是通过SaltClient提交任务到ReqServer的`TCP：4506`端口，并且监听在EventPublisher上获取结果。
2. ReqServer实现了一个MWorkers多进程模型。ReqServer收到请求后发给其中一个MWorker进行处理。
3. MWorker做权限检查后将任务加密发送给Publisher，并且把这个事件发送给EventPublisher。
4. 所有Minion都事先连接到了Publisher的`TCP：4505`端口上，获取到任务后解密处理。Minion处理完毕后将结果发送到Master的ReqServer的`TCP：4506`端口。
5. ReqServer又把这个结果发给了其中一个MWorker进行处理。
6. MWorker拿到结果后进行解密，然后发送到EventPublisher。
7. 此时SaltClient监听在EventPublisher上等待获取结果，碰到结果来了或者超时，命令行返回。

## 3.1. 任务流程图

![](/static/imgs/saltstack_event_arch.jpg)

## 3.2. 提交任务

* 入口 `salt/scripts/salt.py`
* 调用 `salt/salt/scripts.py: salt_main() `
* 调用 `salt/salt/cli/salt.py: SaltCMD:run()`
   1. 判断是否为异步任务，若是，`jid = local.cmd_async(**kwargs)`
   2. 若否，则进行同步执行
* 同步执行

```python

    #
    for full_ret in local.cmd_cli(**kwargs):
         ret_, out, retcode = self._format_ret(full_ret)
         ret.update(ret_)

```


* `local.cmd_cli`调用 `salt/salt/client/__init__.py: LocalClient:cmd_cli()`
* `cmd_cli()`调用`pub_data = self.run_job()` -> `self.pub()` 往ReqServer的`ret_port：tcp4506`端口提交任务请求。

```python

    #
    def pub():
        master_uri = 'tcp://' + salt.utils.ip_bracket(self.opts['interface']) + \
                     ':' + str(self.opts['ret_port'])
        channel = salt.transport.Channel.factory(self.opts,
                                                 crypt='clear',
                                                 master_uri=master_uri)

        try:
            payload = channel.send(payload_kwargs, timeout=timeout)
        except SaltReqTimeoutError:
            raise SaltReqTimeoutError(
                'Salt request timed out. The master is not responding. '
                'If this error persists after verifying the master is up, '
                'worker_threads may need to be increased.'
            )

```

这里的`salt.transport.Channel.factory`最终会被实例化为`AsyncZeroMQReqChannel`，而且实例化的参数中有crypt='clear', 这就意味着，LocalClient给Master发送的消息都是Clear的，也就是未AES加密的。

任务内容的组装在`salt/client/__init__.py`的`def _prep_pub`方法里。其中`cmd: 'publish'`会在接下来的流程里用到。

```python

    #
    def _prep_pub():
    ...
        payload_kwargs = {'cmd': 'publish',
                          'tgt': tgt,
                          'fun': fun,
                          'arg': arg,
                          'key': self.key,
                          'tgt_type': expr_form,
                          'ret': ret,
                          'jid': jid}

```


最终在payload外包装上'enc': 'clear'是在`AsyncZeroMQReqChannel `里的send方法实现的，然后调用`_crypted_transfer`函数里加上。

```python

    #
     @tornado.gen.coroutine
        def send(self, load, tries=3, timeout=60):
            '''
            Send a request, return a future which will complete when we send the message
            '''
            if self.crypt == 'clear':
                ret = yield self._uncrypted_transfer(load, tries=tries, timeout=timeout)
            else:
                ret = yield self._crypted_transfer(load, tries=tries, timeout=timeout)
            raise tornado.gen.Return(ret)


```


最终提交到4506端口的数据变成了类似这样的：

```json
    #
    {'enc': 'clear',
     'load': {'arg': [],
              'cmd': 'publish',
              'fun': 'test.ping',
              'jid': '',
              'key': 'alsdkjfa.,maljf-==adflkjadflkjalkjadfadflkajdflkj',
              'kwargs': {'show_jid': False, 'show_timeout': False},
              'ret': '',
              'tgt': 'client.jacky.com',
              'tgt_type': 'glob',
              'user': 'sudo_vagrant'}}


```

* 提交完任务后，`cmd_cli()`就调用 `self.get_cli_event_returns()`
* 调用 `self.get_iter_returns()`
   1. 判断是否是MoM结构，若是`ret_iter = self.get_returns_no_block('(salt/job|syndic/.*)/{0}'.format(jid), 'regex')`
   2. 若否，`ret_iter = self.get_returns_no_block('salt/job/{0}'.format(jid))`
* `self.get_returns_no_block`中

```python

    #
    while True:
        raw = self.event.get_event(wait=0.01, tag=tag, match_type=match_type, full=True, no_block=True)
        yield raw

```

* 调用了`salt/utils/event.py：SaltEvent:get_event()`, `get_event`又调用了`_get_event()`, 在里面其以SUB的角色连接到了EventPublish监听任务结果的消息。

提交的任务的event内容是

```python

    #
    [DEBUG   ] Sending event - data = {'tgt_type': 'glob', 'jid': '20151123220104386580', 'tgt': 'client.jacky.com', '_stamp'
    : '2015-11-23T14:01:04.386948', 'user': 'sudo_vagrant', 'arg': [], 'fun': 'test.ping', 'minions': ['client.jacky.com']}

```


这是salt命令后提交任务的debug输出

```

    #
     [root@master base]# salt 'client.jacky.com' test.ping -l debug
    [DEBUG   ] Reading configuration from /etc/salt/master
    [DEBUG   ] Missing configuration file: /root/.saltrc
    [DEBUG   ] Configuration file path: /etc/salt/master
    [WARNING ] Insecure logging configuration detected! Sensitive data may be logged.
    [DEBUG   ] Reading configuration from /etc/salt/master
    [DEBUG   ] Missing configuration file: /root/.saltrc
    [DEBUG   ] MasterEvent PUB socket URI: ipc:///var/run/salt/master/master_event_pub.ipc
    [DEBUG   ] MasterEvent PULL socket URI: ipc:///var/run/salt/master/master_event_pull.ipc
    [DEBUG   ] Initializing new AsyncZeroMQReqChannel for ('/etc/salt/pki/master', 'master.jacky.com_master', 'tcp://127.0.0.1:4506', 'clear')
    [DEBUG   ] LazyLoaded config.option
    [DEBUG   ] get_iter_returns for jid 20151124092621201574 sent to set(['client.jacky.com']) will timeout at 09:26:26.241828
    [DEBUG   ] jid 20151124092621201574 return from client.jacky.com

    client.jacky.com:
    	True
    [DEBUG   ] jid 20151124092621201574 found all minions set(['client.jacky.com'])

```

## 3.3. ReqServer实现的多进程模型

ReqServer的启动入口在`salt/master.py`里。

```python

    #
    req_channels = []
    for transport, opts in iter_transport_opts(self.opts):
        chan = salt.transport.server.ReqServerChannel.factory(opts)
        chan.pre_fork(self.process_manager)
        req_channels.append(chan)

```

利用ReqServerChannel的工厂函数实例化ZeroMQ或Raet等其他协议的通信通道，具体的实现在`salt/transport/zeromq.py`里。
`chan.pre_fork(self.process_manager)` -> `process_manager.add_process(self.zmq_device)`, 在`zmq_device`实现了Router＋Dealer的模型，并且Client(Router)绑定了`tcp://ip:4506`端口，Worker(Dealer)根据`ipc_mode`的配置绑定了`tcp://127.0.0.1:4515`或者`ipc://workers.ipc`。

```python

    #
    while True:
        try:
            zmq.device(zmq.QUEUE, self.clients, self.workers)
        except zmq.ZMQError as exc:
            if exc.errno == errno.EINTR:
                continue
            raise exc

```

`zmq.device`对clients和worker之间的消息传递进行了代理。

```python

    #
    for ind in range(int(self.opts['worker_threads'])):
        self.process_manager.add_process(MWorker,
                                         args=(self.opts,
                                               self.master_key,
                                               self.key,
                                               req_channels,
                                               ),
                                         )
    self.process_manager.run()

```

根据配置文件里`worker_threads `的配置启动相应个数的MWorker。

关于ZeroMQReqServerChannel的实现在`salt/transport/zeromq.py`中。客户端会通过`AsyncReqMessageClient`往Router：4506端口提交请求。MWorker继承自`multiprocessing.Process`，每个MWorker被创建的时候都传入了`req_channels `，在run()方法里调用了self.__bind(), 通过post_fork()创建了REP类型的连接到Dealer上，等待处理任务。

```python

    #
    def __bind(self):
        '''
        Bind to the local port
        '''
        # using ZMQIOLoop since we *might* need zmq in there
        zmq.eventloop.ioloop.install()
        self.io_loop = zmq.eventloop.ioloop.ZMQIOLoop()
        for req_channel in self.req_channels:
            req_channel.post_fork(self._handle_payload, io_loop=self.io_loop)  # TODO: cleaner? Maybe lazily?
        self.io_loop.start()

```

至此，这样一个多进程模型就创建完毕。(该图来自ZeroMQ官网)

![](/static/imgs/zeromq_fig17.png)

## 3.4. MWorker的处理逻辑

MWorker的启动入口在`salt/master.py`里。

程序入口是run()方法。设置了`self.clear_funcs`和`self.aes_funcs`方法，并且调用`__bind`方法，通过`post_fork()`传入了`self._handle_payload`任务处理函数，并且创建了REP类型的连接到Dealer上，等待处理任务。

```python

    ＃
    def __bind(self):
        '''
        Bind to the local port
        '''
        # using ZMQIOLoop since we *might* need zmq in there
        zmq.eventloop.ioloop.install()
        self.io_loop = zmq.eventloop.ioloop.ZMQIOLoop()
        for req_channel in self.req_channels:
            req_channel.post_fork(self._handle_payload, io_loop=self.io_loop)  # TODO: cleaner? Maybe lazily?
        self.io_loop.start()

```

`post_fork()`里调用ZeroMQReqServerChannel或者其他ReqServerChannel的实现，以ZeroMQReqServerChannel的post_fork为例，处理任务的入口在这几行代码, 设置了任务处理函数 payload_handler。self.handle_message是MWorker在接收到消息时的一个回调函数，在里面调用了payload_handler去处理任务。

```python

    ＃
    salt.transport.mixins.auth.AESReqServerMixin.post_fork(self, payload_handler, io_loop)

    self.stream = zmq.eventloop.zmqstream.ZMQStream(self._socket, io_loop=self.io_loop)
    self.stream.on_recv_stream(self.handle_message)

```

通过`_handle_payload`方法，我们可以看到`cmd: 'publish'`, 那么MWorker就会调用`self._handle_clear.publish`方法，将任务load发送到PubServerChannel的PULL接口。

```python

    ＃
    @tornado.gen.coroutine
    def _handle_payload(self, payload):
        '''
        The _handle_payload method is the key method used to figure out what
        needs to be done with communication to the server

        Example cleartext payload generated for 'salt myminion test.ping':

        {'enc': 'clear',
         'load': {'arg': [],
                  'cmd': 'publish',
                  'fun': 'test.ping',
                  'jid': '',
                  'key': 'alsdkjfa.,maljf-==adflkjadflkjalkjadfadflkajdflkj',
                  'kwargs': {'show_jid': False, 'show_timeout': False},
                  'ret': '',
                  'tgt': 'myminion',
                  'tgt_type': 'glob',
                  'user': 'root'}}

        :param dict payload: The payload route to the appropriate handler
        '''
        key = payload['enc']
        load = payload['load']
        ret = {'aes': self._handle_aes,
               'clear': self._handle_clear}[key](load)
        raise tornado.gen.Return(ret)

    def _handle_clear(self, load):
        '''
        Process a cleartext command

        :param dict load: Cleartext payload
        :return: The result of passing the load to a function in ClearFuncs corresponding to
                 the command specified in the load's 'cmd' key.
        '''
        log.trace('Clear payload received with command {cmd}'.format(**load))
        if load['cmd'].startswith('__'):
            return False
        return getattr(self.clear_funcs, load['cmd'])(load), {'fun': 'send_clear'}

```



## 3.5. Publisher实现的Pub-Sub任务分发机制

Publisher的入口在`salt/master.py`里。

在Master的启动过程中start()函数里，创建了PubServerChannel，根据传入参数不同创建ZeroMQPubServerChannel或者其他协议的实现，具体的实现在`salt/transport/zeromq.py`里。这里以PubServerChannel为例。

```python

    ＃
    for transport, opts in iter_transport_opts(self.opts):
        chan = salt.transport.server.PubServerChannel.factory(opts)
        chan.pre_fork(process_manager)
        pub_channels.append(chan)

```



```python

    ＃
    def pre_fork(self, process_manager):
        '''
        Do anything necessary pre-fork. Since this is on the master side this will
        primarily be used to create IPC channels and create our daemon process to
        do the actual publishing

        :param func process_manager: A ProcessManager, from salt.utils.process.ProcessManager
        '''
        process_manager.add_process(self._publish_daemon)

```

实例化chan后，调用pre_fork方法，利用`_publish_daemon`方法启动新Daemon进程，监听了pull_uri, pub_uri，并且在while循环里将pull_uri接收到的任务转发到pub_uri里。


```python

    #
    def _publish_daemon(self):
    ...
       while True:
            # Catch and handle EINTR from when this process is sent
            # SIGUSR1 gracefully so we don't choke and die horribly
            try:
                package = pull_sock.recv()
                unpacked_package = salt.payload.unpackage(package)
                payload = unpacked_package['payload']
                if self.opts['zmq_filtering']:
                    # if you have a specific topic list, use that
                    if 'topic_lst' in unpacked_package:
                        for topic in unpacked_package['topic_lst']:
                            # zmq filters are substring match, hash the topic
                            # to avoid collisions
                            htopic = hashlib.sha1(topic).hexdigest()
                            pub_sock.send(htopic, flags=zmq.SNDMORE)
                            pub_sock.send(payload)
                            # otherwise its a broadcast
                    else:
                        # TODO: constants file for "broadcast"
                        pub_sock.send('broadcast', flags=zmq.SNDMORE)
                        pub_sock.send(payload)
                else:
                    pub_sock.send(payload)
            except zmq.ZMQError as exc:
                if exc.errno == errno.EINTR:
                    continue
                raise exc

```


MWorker将任务提交到Publisher是在`self._handle_clear.publish`方法里实现的。

```python

    #
    def publish():
    ...
         # Send it!
        self._send_pub(payload)
    ...

    def _send_pub(self, load):
        '''
        Take a load and send it across the network to connected minions
        '''
        for transport, opts in iter_transport_opts(self.opts):
            chan = salt.transport.server.PubServerChannel.factory(opts)
            chan.publish(load)

```

这里的chan就是ZeroMQPubServerChannel的实例，调用该实例的publish方法，将payload加密，然后发送给Publisher的pull_uri，即`publish_pull.ipc`端口。

```python

    #
    payload = {'enc': 'aes'}

    crypticle = salt.crypt.Crypticle(self.opts, salt.master.SMaster.secrets['aes']['secret'].value)
    payload['load'] = crypticle.dumps(load)

    ...
    pub_sock.connect(pull_uri)

    ...

    pub_sock.send(self.serial.dumps(int_payload))
    ...

```

这是Master上的debug输出

```
    [DEBUG   ] Sending event - data = {'_stamp': '2015-11-24T00:39:00.185467', 'minions': ['client.jacky.com']}
    [DEBUG   ] Sending event - data = {'tgt_type': 'glob', 'jid': '20151124083900185051', 'tgt': 'client.jacky.com', '_stamp': '2015-11-24T00:39:00.186134', 'user': 'sudo_vagrant', 'arg': [], 'fun': 'test.ping', 'minions': ['client.jacky.com']}
    [INFO    ] User sudo_vagrant Published command test.ping with jid 20151124083900185051
    [DEBUG   ] Published command details {'tgt_type': 'glob', 'jid': '20151124083900185051', 'tgt': 'client.jacky.com', 'ret': 'mysql', 'user': 'sudo_vagrant', 'arg': [], 'fun': 'test.ping'}
    [INFO    ] Got return from client.jacky.com for job 20151124083900185051
    [DEBUG   ] Sending event - data = {'fun_args': [], 'jid': '20151124083900185051', 'return': True, 'retcode': 0, 'success': True, 'cmd': '_return', '_stamp': '2015-11-24T00:39:00.303857', 'fun': 'test.ping', 'id': 'client.jacky.com'}


```

## 3.6. Minion连接到Publisher获取和处理任务

Minion在启动过程中最终会进入`tune_in`方法，然后陷入无限循坏，不断处理任务和返回结果。实现在`salt/minion.py`里。

* `tune_in`调用`self.connect_master`
* `connect_master`调用`self.eval_master(self.opts, self.timeout, self.safe)`
* `eval_master`中利用AsyncPubChannel的factory方法，根据不同参数实例化相应的`pub_channel`，这里以AsyncZeroMQPubChannel为例，具体的实现在`salt/transport/zeromq.py`里。

```python
    #
    try:
        pub_channel = salt.transport.client.AsyncPubChannel.factory(opts, **factory_kwargs)
        yield pub_channel.connect()
        conn = True
        break
    except SaltClientError:
        msg = ('Master {0} could not be reached, trying '
               'next master (if any)'.format(opts['master']))
        log.info(msg)
        continue

```

* 调用AsyncZeroMQPubChannel的connect方法，以SUB的角色连接到Master的PUB端口4505。

    ```python

        #
        def connect(self):
            if not self.auth.authenticated:
                yield self.auth.authenticate()
            self.publish_port = self.auth.creds['publish_port']
            self._socket.connect(self.master_pub)

    ```

* `tune_in`方法里，连接到Master之后，设置任务处理的回调函数

```python

    #
    # add handler to subscriber
    self.pub_channel.on_recv(self._handle_payload)

```

* 在`pub_channel.on_recv`其实就是`AsyncZeroMQPubChannel.on_recv()`方法，封装了对收到的message进行解密。

```python

     #
     def on_recv():
             @tornado.gen.coroutine
            def wrap_callback(messages):
                payload = yield self._decode_messages(messages)
                if payload is not None:
                    callback(payload)

```

`self._decode_messages()`调用了`self._decode_payload()`进行解密。见`salt/transport/mixins/auth.py`的`class AESPubClientMixin(object)`。

```python

    #
    @tornado.gen.coroutine
    def _decode_payload(self, payload):
        # we need to decrypt it
        log.trace('Decoding payload: {0}'.format(payload))
        if payload['enc'] == 'aes':
            self._verify_master_signature(payload)
            try:
                payload['load'] = self.auth.crypticle.loads(payload['load'])
            except salt.crypt.AuthenticationError:
                yield self.auth.authenticate()
                payload['load'] = self.auth.crypticle.loads(payload['load'])

        raise tornado.gen.Return(payload)


```

* `self._handle_payload`调用了`_handle_decoded_payload`，根据`data['fun']`的类型初始化target，接下来以target创建新的进程或者线程去处理这个任务（根据master里multiprocessing参数来判断是创建新进程还是线程）。具体处理逻辑在`_thread_return`或者`_thread_multi_return`里，这里以`_thread_return`为例。

    ```python

        #
        if isinstance(data['fun'], tuple) or isinstance(data['fun'], list):
            target = Minion._thread_multi_return
        else:
            target = Minion._thread_return

    ```

* `_thread_return`中对任务进行处理，然后用`minion_instance._return_pub`返回结果给Master的4506端口。

```python

    #
    try:
        func = minion_instance.functions[data['fun']]
        args, kwargs = load_args_and_kwargs(
            func,
            data['arg'],
            data)
        minion_instance.functions.pack['__context__']['retcode'] = 0
        if opts.get('sudo_user', ''):
            sudo_runas = opts.get('sudo_user')
            if 'sudo.salt_call' in minion_instance.functions:
                return_data = minion_instance.functions['sudo.salt_call'](
                        sudo_runas,
                        data['fun'],
                        *args,
                        **kwargs)
        else:
            return_data = func(*args, **kwargs)

```

* `_return_pub`方法中调用`salt.transport.Channel`的factory工厂方法实例化到master到连接，这里的channel就是AsyncZeroMQReqChannel，使用`channel.send`方法将结果发送。

```python

    #
    def _return_pub():
    ...
        channel = salt.transport.Channel.factory(self.opts)
    ...
            try:
            ret_val = channel.send(load, timeout=timeout)
        except SaltReqTimeoutError:
            msg = ('The minion failed to return the job information for job '
                   '{0}. This is often due to the master being shut down or '
                   'overloaded. If the master is running consider increasing '
                   'the worker_threads value.').format(jid)
            log.warn(msg)
            return ''

```

这里的`AsyncZeroMQReqChannel.send`默认会使用aes加密的方式对消息进行发送。

```python

    #
     @tornado.gen.coroutine
        def send(self, load, tries=3, timeout=60):
            '''
            Send a request, return a future which will complete when we send the message
            '''
            if self.crypt == 'clear':
                ret = yield self._uncrypted_transfer(load, tries=tries, timeout=timeout)
            else:
                ret = yield self._crypted_transfer(load, tries=tries, timeout=timeout)
            raise tornado.gen.Return(ret)


```

这是Minion上的debug输出

```python

    #
     [INFO    ] User sudo_vagrant Executing command test.ping with jid 20151124083900185051
    [DEBUG   ] Command details {'tgt_type': 'glob', 'jid': '20151124083900185051', 'tgt': 'client.jacky.com', 'ret': 'mysql', 'user': 'sudo_vagrant', 'arg': [], 'fun': 'test.ping'}
    [INFO    ] Starting a new job with PID 27556
    [DEBUG   ] LazyLoaded test.ping
    [DEBUG   ] Minion return retry timer set to 2 seconds (randomized)
    [INFO    ] Returning information for job: 20151124083900185051
    [DEBUG   ] Initializing new AsyncZeroMQReqChannel for ('/etc/salt/pki/minion', 'client.jacky.com', 'tcp://192.168.33.20:4506', 'aes')
    [DEBUG   ] Initializing new SAuth for ('/etc/salt/pki/minion', 'client.jacky.com', 'tcp://192.168.33.20:4506')

```

## 3.7. SaltClient将结果返回

在3.1里讲到了Client以SUB的角色连接到了Master的EventPublisher上监听结果。自此，执行一个命令的闭环就完成了。

# 4. 小结

分析完这个流程，几点值得学习的地方是

1. 如何利用ZeroMQ实现各种进程通信模型
1. 如何用Python实现大型基础架构软件

# 5. 参考资料

1. [Salt Development Architecture Overview](https://docs.saltstack.com/en/latest/topics/development/architecture.html)
1. [Saltstack github](https://github.com/saltstack/salt)
