---
layout : post
title : 【 python 基础系列 】 Pickle 的使用
category : python
date : 2018-02-02
tags : [python, Pickle]
---

> 原文：[储存你的对象](https://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/a-guide-to-pythons-magic-methods.html#id22)

如果你接触过其他的 python 开发者，你可能已经听说过 Pickle 了， Pickle 是用来序列化 Python 数据结构的模块，在你需要暂时存储一个对象的时候（比如缓存），这个模块非常的有用，不过这同时也是隐患的诞生地。

序列化数据是一个非常重要的功能，所以他不仅仅拥有相关的模块（ Pickle , cPickle ），还有自己的协议以及魔术方法，不过首先，我们先讨论下关于序列化内建数据结构的方法。

## Pickling: 简单例子

让我们深入研究 Pickle，比如说你现在需要临时储存一个字典，你可以把它写入到一个文件里，并且要小心翼翼的确保格式正确，之后再用 exec() 或者处理文件输入来恢复数据，实际上这是很不安全的，如果你使用文本存储了一些重要的数据，任何方式的改变都可能会影响到你的程序，轻则程序崩溃，重则被恶意程序利用，所以，让我们用 Pickle 代替这种方式：

```python 
import pickle

data = {'foo': [1, 2, 3],
        'bar': ('Hello', 'world!'),
        'baz': True}
jar = open('data.pkl', 'wb')
pickle.dump(data, jar) # write the pickled data to the file jar
jar.close()
嗯，过了几个小时之后，我们需要用到它了，只需把它 unpickle 了就行了：

import pickle

pkl_file = open('data.pkl', 'rb') # connect to the pickled data
data = pickle.load(pkl_file) # load it into a variable
print data
pkl_file.close()
```

正如你期望的，数据原封不动的回来了！

## 忠告 

同时要给你一句忠告： pickle 并不是很完美， Pickle 文件很容易被不小心或者故意损坏， Pickle 文件比纯文本文件要稍微安全一点，但是还是可以被利用运行恶意程序。 Pickle 不是跨版本兼容的（译注：最近刚好在 《Python Cookbook》上看到相关讨论，书中描述的 Pickle 是跨版本兼容的，此点待验证），所以尽量不要去分发 Pickle 过的文本，因为别人并不一定能够打开。不过在做缓存或者其他需要序列化数据的时候， Pickle 还是很有用处的。