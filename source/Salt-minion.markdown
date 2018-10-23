---
layout : post
title : salt minion 启动问题
category : QA
date : 2016-01-18 19:55:00
tags : [QA, salt]
---



### Q & A：

修改minion 的配置文件中master 的值后，启动报错，如下：

    Traceback (most recent call last):
      File "/usr/lib/python2.6/site-packages/salt/scripts.py", line 81, in minion_process
        minion.start()
      File "/usr/lib/python2.6/site-packages/salt/cli/daemons.py", line 277, in start
        self.minion.tune_in()
      File "/usr/lib/python2.6/site-packages/salt/minion.py", line 1648, in tune_in
        self.sync_connect_master()
      File "/usr/lib/python2.6/site-packages/salt/minion.py", line 720, in sync_connect_master
        self.io_loop.start()
      File "/usr/lib64/python2.6/site-packages/zmq/eventloop/ioloop.py", line 151, in start
        super(ZMQIOLoop, self).start()
      File "/usr/lib64/python2.6/site-packages/tornado/ioloop.py", line 809, in start
        self._run_callback(callback)
      File "/usr/lib64/python2.6/site-packages/tornado/ioloop.py", line 591, in _run_callback
        ret = callback()
      File "/usr/lib64/python2.6/site-packages/tornado/stack_context.py", line 274, in null_wrapper
        return fn(*args, **kwargs)
      File "/usr/lib64/python2.6/site-packages/tornado/gen.py", line 963, in <lambda>
        self.future, lambda f: self.run())
      File "/usr/lib64/python2.6/site-packages/tornado/gen.py", line 879, in run
        yielded = self.gen.send(value)
      File "/usr/lib/python2.6/site-packages/salt/crypt.py", line 553, in sign_in
        raise SaltSystemExit('Invalid master key')
    SaltSystemExit: Invalid master key


<!-- more -->
### 引起原因

认证key的错误造成。

### 解决方案：

- 1、删除 `/etc/salt/pki` 目录，

- 2、重启 minion，在master端认证即可。





