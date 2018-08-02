<!-- TOC -->

- [Python语言简介](#python语言简介)
    - [Python介绍及发展](#python介绍及发展)
        - [介绍](#介绍)
        - [历史](#历史)
        - [Python2 vs Python3](#python2-vs-python3)
    - [Python的优劣及应用领域](#python的优劣及应用领域)
        - [应用领域](#应用领域)
    - [与其他语言比较](#与其他语言比较)
    - [如何学习Python](#如何学习python)
- [参考](#参考)

<!-- /TOC -->

## Python语言简介

### Python介绍及发展

#### 介绍

Python 官方网站：https://www.python.org/， 大家可以到此处下载 Python和查看 Python的官方文档和相关资讯。

对应 Python的介绍，官方网站是这样描述描述的：

>Python 是一款易于学习且功能强大的编程语言。它具有高效率的数据结构，能够简单又有效地实现面向对象编程。Python 简洁的语法与动态输入之特性，加之其解释性语言的本质，使得它成为一种在多种领域与绝大多数平台都能进行脚本编写与应用快速开发工作的理想语言。

大家可以这样理解：
- python 易于学习，功能强大
- 语法简洁
- 应用广泛，多个系统平台使用
- 开发快速

这里有几个需要讲解的概念：
- 数据结构
- 面向对象
- 动态输入
- 解释语言

这几个概念大家可以先记着，后面的会随着我们的课程慢慢展开讲解，这里不做赘述。

那么这么优秀的一款语言是怎么来的？它主要应用在哪些领域？与其他语言相比较有什么优劣呢？我们带着这些问题继续阅读。

#### 历史

![](https://ws1.sinaimg.cn/large/8697aaedly1frvs8rhblhj208b07tq7g.jpg)

Python的作者，吉多·范罗苏姆(Guido von Rossum)，荷兰人，业内人称龟叔。

Guido 当时在荷兰的 CWI（Centrum Wiskunde & Informatica) 研究所工作，在一个叫 `分布式操作系统Amoeba` 项目组中。当时项目组正需要一种简单、易扩展且跨平台的脚本语言。Guido想到了之前参与的 ABC 项目，当时他介于ABC语言的复杂，曾经尝试设计一款简单的脚本语言。于是，在1989年的圣诞节，Guido便开始编写Python语言的编译器。Python这个名字，来自Guido所挚爱的电视剧《Monty Python’s Flying Circus》。他希望这个新的叫做Python的语言，能符合他的理想：创造一种C和shell之间，功能全面，易学易用，可拓展的语言。

在早期，Guido 和他的同事作为python的核心开发者和使用者，后来逐渐扩展到团队外。python早期通过邮件列表来进行交流和开发，用户将改动发给Guido, 有他来决定是否将这些新特性添加到python，因为至高无上的决策权，被称为“终身的仁慈独裁者”。随着社区的形成壮大，python的开发方式逐渐转为开源的方式，遵循 GPL(GNU General Public License)协议并通过一套PEP文档的审核流程来合作开发。从此，python的开发工作被社区大部分人分担，但Guido 作为核心开发者，仍决定着python的发展走向。


**Python 发展时间线：**

- 1989年圣诞节， Guido von Rossum开始写Python语言的编译器。
- 1991年2月，第一个Python编译器（同时也是解释器）诞生，它是用C语言实现的（后面又出现了Java和C#实现的版本Jython和IronPython，以及PyPy、Brython、Pyston等其他实现），可以调用C语言的库函数。在最早的版本中，Python已经提供了对“类”，“函数”，“异常处理”等构造块的支持，同时提供了“列表”和“字典”等核心数据类型，同时支持以模块为基础的拓展系统。
- `Python 1.0` 1994年1月正式发布。
- `Python 2.0` 2000年10月16日发布，增加了实现完整的垃圾回收，并且支持Unicode。与此同时，Python的整个开发过程更加透明，社区对开发进度的影响逐渐扩大，生态圈开始慢慢形成。python2.0变化最大的可能不是代码，而是开发方式。

- `Python2.4` 2004年11月30发布，是python2.x的经典实用版本。2005年，目前为止 python中最流行的框`Django` 发布。
- `Python 3.0` 2008年12月3日发布，此版不完全兼容之前的Python代码，不过很多新特性后来也被移植到旧的Python 2.6/2.7版本，因为目前还有公司在项目和运维中使用Python 2.x版本的代码。回归初衷，“有且仅有唯一的解决方案”。

- `Python2.6 ` 2008年10月发布。随后，增加了许多兼容python3的语法，和随后发布的2.7成为2.x的过度版本。
- `Python2.7` 2010年7月发布。同年，python中流行的`Flask`框架发布，一经发布便以它简单、自定义的特性迅速蹿红。现在已与Django 并驾齐驱成为python界最受欢迎的2大web框架。

- 2014年4月 Guido [宣布](https://hg.python.org/peps/rev/76d43e52d978)Python 2.7支持时间延长到2020年。且不会再有2.8了。
>[pep0373](https://www.python.org/dev/peps/pep-0373/)描述：
>Being the last of the 2.x series, 2.7 will have an extended period of maintenance. Specifically, 2.7 will receive bugfix support until January 1, 2020. All 2.7 development work will cease in 2020.
>There will be no Python 2.8 (see [PEP 404](https://www.python.org/dev/peps/pep-0404)).

- `python3.6` 2016年12月发布。
- `python3.6.5` 2018年3月发布，截止目前3.x的最新版本。本教程中所有示例均基于此版本。

更详细的发布列表参阅[官网](https://www.python.org/doc/versions/)

Python的版本号分为三段，形如A.B.C。其中A表示大版本号，一般当整体重写，或出现不向后兼容的改变时，增加A；B表示功能更新，出现新功能时增加B；C表示小的改动（如修复了某个Bug），只要有修改就增加C。

扩展阅读：

- [python 简史](http://www.15yan.com/story/1JKTBQvVk5e/)
- [python 百科](https://en.wikipedia.org/wiki/Python_(programming_language))


#### Python2 vs Python3

[Brett Cannon](https://snarky.ca/) Python的核心开发者，在Puppy上的问答，回答了[为什么会有Python3?](http://www.snarky.ca/why-python-3-exists)，大体意思如下：

由于python发布的时间早于 Unicode标准协议等一些相应标准的发布时间，造成截止到python2.x 时并不能很好的支持Unicode编码。针对此问题Python的开发者们发布了python3。除了Unicode的问题，python3还对python2做了很多优化。Python 官方网站是这样描述python2与python3的关系的"Python 2.x是遗留的，Python 3.x是该语言的现在和未来"。

之前人们还有疑虑说python3各种不兼容，随着越来越多的库迁移到`python3.x`，当前python3已经相当成熟。我们现在开始学习python的话，完全可以直接学习python3.x。本教程所有实例均是基于python3.6, 请大家注意版本。


扩展阅读：

- [为什么会有python3](https://snarky.ca/why-python-3-exists/)
- [Should I use Python 2 or Python 3 for my development activity?](https://wiki.python.org/moin/Python2orPython3)

### Python的优劣及应用领域

简单易学习、开发源码、跨平台、扩展性和嵌入型强、代码规范，可读性强

Python的优点很多，简单的可以总结为以下几点。

- 简单和明确，做一件事只有一种方法。
- 学习曲线低，与其他很多语言比上手更容易。
- 开放源代码，拥有强大的社区和生态圈。
- 解释型语言，完美的平台可移植性。
- 支持两种主流的编程范式，可以使用面向对象和函数式编程。
- 可扩展性和可嵌入性，可以调用C/C++代码也可以在C/C++中调用。
- 代码规范程度高，可读性强，适合有代码洁癖和强迫症的人群。

Python的缺点主要集中在以下几点。

- 执行效率低下，因此计算密集型任务可以由C/C++编写。
- 代码无法加密，但是现在的公司很多都不是卖软件而是卖服务，这个问题慢慢会淡化。
- 在开发时可以选择的框架太多，有选择的地方就有错误。


#### 应用领域

目前几个比较流行的计算机领域，Python都有用武之地。

>- 云基础设施 - Python / Java / Go
>- DevOps - Python / Shell / Ruby / Go
>- 网络爬虫 - Python / PHP / C++
>- 数据分析挖掘 - Python / R / Scala / Matlab
>- 机器学习 - Python / R / Java / Lisp

应用的企业的也是越来越多，国内有豆瓣、搜狐、金山、通讯、盛大、网易、百度、阿里、土豆、新浪等，国外有Google、NASA(美国国家航空和宇宙航行局)、YOUTUBe、FACEBOOK、红帽、Instagram等企业都在广泛应用。

扩展阅读：
- https://www.quora.com/What-is-the-biggest-company-that-uses-Python-Flask
- https://www.quora.com/Which-Internet-companies-use-Python


### 与其他语言比较
- C 语言，1973 年发布，有贝尔实验室（C、C++、unix出自于此）的计算机科学家丹尼斯·里奇（Dennis Ritchie）创造的。应用广泛的的高级编程语言的高级编程语言。
    - 优点：运行速度快、片底层对机器控制友好，在嵌入式、硬件驱动、游戏开发有广发应用。
    - 缺点：学习成本高、开发效率低。
- C++ ， 1983年正式命名。是C语言的升级版，增加了面向对象等特性。提升了开发效率。
- Java , 1995年Sun公司正式发布。由Oak语言改名而来，1992年已开发成功。
    - 优点：面向对象，学习成本比C语言低、跨平台、稳定性
    - 缺点：随着Java应用的增大，其体系庞大、语法变得复杂多变。
- C#, 2000年微软发布，20世纪初，微软公司开发的一款面向对象的语言。.NET Framework平台的核心语言。
    - 优点：面向对象，较简单的语言特性，稳定性。
    - 缺点：运行效率较低、除window外系统支持有限。
- GO, 2009年 Google 发布，在不损失性能的情况下极大的降低了代码复杂度。将是Python语言的有力竞争者。

### 如何学习Python

- 1、循序渐进，跟着课程一步一步来。

- 2、大家在除了每章后边联系题之外。需要去多联系，在联系的时候呢，要输入代码，不要复制、粘贴。有问题呢，可以查阅官方文档或咨询老师。

- 3、阅读别人的代码，吸收它的有点，避免它烦的错误。


## 参考

- [人生苦短，只需一部Python简史](https://www.douban.com/note/543082723/)
- [https://github.com/jackfrued/Python-100-Days/blob/master/Day01-15/Day02/%E8%AF%AD%E8%A8%80%E5%85%83%E7%B4%A0.md](https://github.com/jackfrued/Python-100-Days/blob/master/Day01-15/Day02/%E8%AF%AD%E8%A8%80%E5%85%83%E7%B4%A0.md)