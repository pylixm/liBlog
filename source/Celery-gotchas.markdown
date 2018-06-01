---
layout : post
title : 译-使用 celery 时的 3 个坑 
category : celery
date : 2016-03-08
tags : [django, celery, 翻译]
old_url : https://wiredcraft.com/blog/3-gotchas-for-celery

---


Celery is our go-to task manager when working with Python. It is feature rich, stable, fast and has clean interfaces. We usually end up using it either for high volumes of short tasks or low volumes of long running ones (understand 10+ seconds, or even minutes in devo.ps’ case).

Celery’s feature set is a double edged sword though; it’s great once you got things set up, but getting there often means some amount of trial and errors. If you’re just getting started, go read “Celery Best Practices” by Deni Bertovic. Once you’re done, come back here and I’ll share a few more tips.


Celery 是Python开发者们常用到的一个任务管理器。它功能丰富，性能稳定，速度快，拥有清晰的接口。

无论是对大批量的短期任务还是长时间运行的任务（10s+，在devo.ps 的情况下甚至几分钟（原文：even minutes in devo.ps’ case) ），

我们都会使用它。

Celery 的功能是把双刃剑。一旦你的东西成功，他就是伟大的；但一旦失败，你就需要不断的尝试去解决错误。

如果你是初学者，建议去读 [“Celery Best Practices” by Deni Bertovic](https://denibertovic.com/posts/celery-best-practices/)。

您完成后，我给大家介绍几个技巧。



### Gotcha 1: You can’t spawn processes from within Celery tasks

You can usually stick to testing (and unit testing hopefully) your tasks outside of Celery. You will however sometimes run into the following error when spawning a process from within a Celery task:

    daemonic processes are not allowed to have children

We ran into this issue when trying to programmatically run Ansible playbooks within Celery. It was tricky to catch because it only surfaced when we upgraded to Celery 3.1.x. Turns out, any code attempting to create sub-processes using the multiprocessing module will fail. That can be hard to prevent or detect since you may not be aware that some of the libraries you use actually do that.

You can find a long thread discussing this on GitHub. It actually worked in older Celery versions (3.0.x) because of a bug masking it. To my understanding this problem arises from unix limitation and how the underlying billiard module is used.

There doesn’t seem to be clean solution for this one, but you can find some possible workarounds in the GitHub issue above. You can also use Celery 3.0.x or simply avoid using libraries that rely on multiprocessing.



### 技巧一， 您不能在celery的任务中创建子进程
 
当你在测试辛辛苦苦写完的 `tasks` 时。当到创建子进程的 `task` 运行时，常会得到如下错误：

    daemonic processes are not allowed to have children

我们尝试在 `celery` 中运行Ansibe playbooks 时，出现了这个错误。这个错误是非常棘手的，在把 `celery` 升级到

3.1.x 后，任务尝试使用 `multiprocessing ` 模块创建子进程的代码都出现错误。这是很难预防和发现的。

你可以再github 上找到很长的讨论。这个问题在老版本的 `celery 3.0.x` 可以运行，我怀疑是新版本的一个 bug 。
    
以我的理解，解决这个问题，应该从UNUIX限制和biliard模块底层来看。

这个问题似乎没有一个简洁的解决方案。但你可以从Github讨论的问题列表中，找到解决方案。你可以继续使用3.0.x 或干脆避免使用 `multiprocessing` 模块。


### Gotcha 2: Limitations on arguments when chaining tasks

We had a chain of Celery tasks where the first one had to pass multiple parameters to the following one. Diving into the documentation, we quickly realized it wasn’t as straightforward as it appeared: by default, each task in the chain will pass (multiple) arguments to the next one as a tuple.



### 技巧二， 任务链中对参数的限制

我们在使用Celery 的任务链时，第一个有多个参数的tasks 会传递给下一个。深入文档，会发现，它似乎不是那么简单。在默认情况下，任务链中任务会通过（多个）
    
参数会作为元组传递给下一个。


This leaves you two options:

Use a decorator on tasks to unpack the tuple or stick to a single argument (possibly a more complex one, e.g a class instance or dictionary).

Our unpack_tuple decorator looks like this:
    
    def unpack_tuple(f):
        @functools.wraps(f)
        def _wrapper(*args, **kwargs):
            if len(args) > 0 and type(args[0]) == tuple:
                args = args[0] + args[1:]
            return f(*args, **kwargs)
        return _wrapper
    And here’s how we used it:
    
    chain(fetch_user.s(userid), process.s())
    
    @task
    def fetch_user(userid)
        # process
        return firstname, lastname
    
    @task
    @unwrap_tuple
    def process(firstname, lastname)
        # Do processing
    
    
### Gotcha 3: Tasks stay queued even when there are free workers

We were running long running tasks (5+ minutes to provision new servers on EC2 & Digital Ocean), usually only one at a time. We quickly noticed that when two tasks, or more, where triggered at the same time, second one would hang until the first one completed, even when we had plenty of available workers.

This is due to the way Celery acknowledges messages from the broker; the first worker would simply reserve the first task, then acknowledge it immediately after starting it, and proceed on reserve the following one.

To deal with it, simply use the following 2 settings:

- `ACKS_LATE=True`: this ensures that the worker acks the task after it’s completed. If the worker crashes, it will just restart.

- `PREFETCH_MULTIPLIER=1`: this ensures that the worker process can reserve at most one un-acked task at a time. If this is used with `ACKS_LATE=False` (the default), the worker will reserve a task as soon as it starts processing the first one.

Beware that setting `PREFETCH_MULTIPLAYER=0` means unlimited prefetching (not disable prefetching).

Understanding how `PREFETCH_MULTIPLAYER` and ACK_LATE work isn’t trivial, I recommend you spend some time reading the official documentation.


附：

[celery 最佳实践](https://denibertovic.com/posts/celery-best-practices/)

[官网问题汇总](http://www.celeryproject.org/community/)


---

**ps: 个人英文水平有限，还请各位批评指正。**
