<!-- TOC -->

- [计算机编程基础知识](#计算机编程基础知识)
    - [编程入门准备知识](#编程入门准备知识)
        - [计算机基本组成](#计算机基本组成)
        - [计算机中的编码](#计算机中的编码)
        - [一门语言的基本组成](#一门语言的基本组成)
- [环境搭建](#环境搭建)
    - [Python下载和安装(window/mac/linux)](#python下载和安装windowmaclinux)
        - [windows 系统安装](#windows-系统安装)
        - [Mac 系统安装](#mac-系统安装)
        - [Linux 系统安装](#linux-系统安装)
    - [交互式环境](#交互式环境)
        - [终端shell](#终端shell)
        - [IDLE](#idle)
        - [ipython](#ipython)
    - [集成式开发环境选择](#集成式开发环境选择)
        - [Sublime](#sublime)
        - [VSCode](#vscode)
        - [PyCharm](#pycharm)
- [总结](#总结)
- [参考](#参考)

<!-- /TOC -->
[< 返回索引页](https://segmentfault.com/a/1190000015378402)

## 计算机编程基础知识

### 编程入门准备知识

#### 计算机基本组成

个人PC计算机系统组成分`硬件`和`软件`量大部分。硬件系统主要由中央处理器、存储器、输入输出控制系统和各种外部设备组成。软件分为系统软件和应用软件。

![](https://ws1.sinaimg.cn/large/8697aaedly1frzheixkmwj20jg0h1ab2.jpg)

图片来源：百度百科

那本教程涉及的部分，为计算机应用软件编程。

#### 计算机中的编码

![](https://ws1.sinaimg.cn/large/8697aaedly1frzhvtuhh0j20g409v0u1.jpg)
第一代电子计算机 - ENIAC

计算机是不能识别人类语言的，那么她们是如何处理任务的呢？计算机归根结底是一种电路设备，她们底层处理都是通过电路的开关来识别。根据这一点，人们就通过将任务指令转化为用0和1的二进制串来标识，从而让计算机系统可以识别。这种直接有二进制代码组成的程序语言叫`机器语言`。后来人们在二级制的机器语言上发明了`汇编语言`，只用指令集来对应不同的机器指令，通过汇编过程转换成机器指令来执行。再后来到20世纪中期，一大批高级语言诞生，包括后来应用广泛的C、VB等语言。

现在我们知道，计算机是使用 0和1 的二进制串来执行指令的。那么这些0和1是如何表示指令的呢? 这便需要一个二进制数据和实际人类语言的一个对应关系，这套对应关系便成为`字符编码`。字符编码使用8个二进制位作为一个单位，叫做一个`字节`，8个二进制位可以标识256中状态。

**ASCII**

上世纪60年代，美国制定了一套字符编码，对英语字符与二进制位之间的关系，做了统一规定。这被称为 ASCII 码，一直沿用至今。

ASCII 码一共规定了128个字符的编码，比如空格SPACE是32（二进制00100000），大写的字母A是65（二进制01000001）。这128个符号（包括32个不能打印出来的控制符号），只占用了一个字节的后面7位，最前面的一位统一规定为0。

随着计算机的普及，ASCII码已经不能满足人们的需求，除英语外的其他语言无法用ASCII编码来映射。于是，各国家自己制定一些编码，如我国制定了简体中文`GB2312`，使用2个字节来标识一个汉字，即可表示256*256=65535个汉字，后来的升级版`GBK`，这种以2个字节来表示的编码成为`ANSI编码`；欧洲国家则使用没有使用的首位二进制位来制定了标识字符的标准。

**Unicode**

随着计算机的发展普及，不统一的编码问题，极大的影响了计算机的发展及交流。Unicode （统一码，万国码）编码此时应运而生，1991年由[统一码联盟](https://zh.wikipedia.org/wiki/%E7%B5%B1%E4%B8%80%E7%A2%BC%E8%81%AF%E7%9B%9F)首次发布标准。他使用2到4个字节来表示一个字符，一个字符的Unicode编码是确定的。Unicode 是一个很大的集合，现在的规模可以容纳100多万个符号，详细可见[Unicode编码表](http://www.unicode.org/charts/)，现在还在完善扩充。

Unicode 只是一个符号集，它只规定了符号的二进制代码，却没有规定这个二进制代码应该如何实现。造成以下问题：
- 1）出现了 Unicode 的多种存储方式，也就是说有许多种不同的二进制实现方式，可以用来表示 Unicode。
- 2）Unicode 在很长一段时间内无法推广，直到互联网的出现，对网络传输中数据的大小要求严格。

**UTF**

Unicode 编码表示同一个字符时，比ASCII码的占用空间大的多，这在网络传输过程中是非常占用资源的。Unicode的实现方式不同于编码方式，是有多重实现方式的，为了节省空间，人们设计了可变长的Unicode实现方式，Unicode的实现方式称为Unicode转换格式（Unicode Transformation Format，简称为UTF）。UTF-8 就是在互联网上使用最广的一种可变长 Unicode 的实现方式。除了UTF-8含有 UTF-16、UTF-32等版本。

总结如下：

- UTF-8： 使用1、2、3、4个字节表示字符；优先使用1个字符、无法满足则使增加一个字节，最多4个字节。英文占1个字节、欧洲语系占2个、东亚占3个，其它及特殊字符占4个
- UTF-16： 使用2、4个字节表示所有字符；优先使用2个字节，否则使用4个字节表示。
- UTF-32： 使用4个字节表示所有字符；

计算机编码基本分类如下：

![](https://ws1.sinaimg.cn/large/8697aaedly1frzj7qhgo5j20ye0q27c9.jpg)

图片来源：[regexlab](http://www.regexlab.com/zh/encoding.htm)

扩展阅读：
- [http://www.regexlab.com/zh/encoding.htm](http://www.regexlab.com/zh/encoding.htm)
- [Unicode](https://zh.wikipedia.org/wiki/Unicode)
- [UTF-8](https://zh.wikipedia.org/wiki/UTF-8)

发展至今，现在计算机中，当内存处理时统一使用了Unicode编码，当需要保存到硬盘或者需要传输的时候，就转换为UTF-8等可变编码。因为UTF编码的可变性，在内存中处理非常耗时，在内存中统一使用Unicode编码，Unicode在编码方式上对应的字符是唯一的。在存储和专属时，UTF编码则更节省空间。

#### 一门语言的基本组成

我们先来看一段Python代码：

```python
name = input('请输入姓名：')

def say_hello(name='Tim'):
    print('%s,hello!'%name)
    
say_hello(name)
```

我们来看下这段程序做了什么事？程序提示我们输入姓名，当我们输入姓名后，程序把我们录入的姓名加工组成了一条语句，打印了出来。在这个过程中，计算机内部是如何运作的呢？程序运行时，它在计算机的内存中开辟了一块空间，用来存储我们接下要录入的信息。当我们输入姓名后，它把姓名和内部定义好的hello拼接在一起，打印了出来。

我们把这种存储可变化的值的对象叫做`变量`。相对应的存储不可变值的对象叫做`常量`。而处理我们输入数据的这块代码叫做`方法`。方法有方法名（say_hello）、参数(name)、和方法体(print)组成。其中最复杂的地方便是这个方法体，这个方法的功能和处理任务的逻辑都在这块。

变量、常量和方法，以及方法体中复杂的控制逻辑语法共同构成了一套基本的编程语言。

## 环境搭建

### Python下载和安装(window/mac/linux)

#### windows 系统安装

window系统可直接从[官网下载地址](https://www.python.org/downloads/windows/)对应操作系统位数的exe安装包，安装即可。

安装时需要注意一下几点：

- 1、选择适合自己操作系统的安装包。
![](./images/choice.png)

- 2、安装时勾选“Add Python 3.6 to PATH”，会将python的安装目录和命令目录一并加到系统环境变量中，这样我们在CMD窗口中才可以使用 `python` 命令。
- 3、点击自定义安装，将python的常用工具包（pip包等）安装上。
- 4、因windows不同操作系统版本，安装可能出现 “xx.dll” 文件缺失的情况，我们到[微软官方](https://www.microsoft.com/zh-cn/download/details.aspx?id=48145)网站下载对应版本自行安装即可。

安装完毕后，打开系统CMD窗口，输入python命令，见到如下信息便说明成功。

![](./images/success.png)

#### Mac 系统安装

mac 系统自带了python2.7。我们开发使用python3.6，那怎么办呢？建议重新安装python3.6，而不是升级系统版本，因为系统python为mac系统自带的许多工具提供了语言环境，我们尽量不要去污染系统自带的python,以免造成系统工具不可用的情况发生。

那如何安装python3.6呢？我们建议使用`brew`mac软件包管理工具统一安装，执行如下命令即可：

```bash
brew install python
```

安装完毕后，在我们的命令行终端中输入python命令检查是否安装成功。

#### Linux 系统安装

Linux系统同mac一样也自带了python。同样建议我们安装自己开发使用的python包，不要污染系统python包。Linux 系统安装比较麻烦,需要我们自己编译安装，具体步骤如下：

- 首先，安装python开发的一些依赖包

```bash
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
```

- 第二，从Python官网下载python的源码包并解压。

```bash

wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz

tar zxvf Python-3.6.5.tgz
```

- 第三，编译安装

```bash
cd Python-3.6.5

./configure --with-ensurepip=install 

make && make install 

```

安装成功后，会在`/usr/local/bin` 路径下增加python3命令，我们运行 `python3` 命令便是执行了我们刚才安装的python，执行`python` 命令则会运行系统自带的python。

同样，在终端运行python3命令检测是否安装成功。

### 交互式环境

#### 终端shell

在命令行终端下，输入 `python` 即打开了python的交换式环境，这是解释性语言特有的。 在此环境下，我们可以直接运行python代码，来做简单的测试。

```
$ python3
Python 3.6.5 (default, Mar 30 2018, 06:42:10)
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> print('hello, world!')
hello, world!
>>>
```

退出交互式环境，使用`exit()`。

#### IDLE

针对于windows用户，python 自带了一个python shell小工具 IDLE。带有代码高亮和提示功能，如图：
![](./images/python_shell.png)
![](./images/python_shell_ts.png)

#### ipython

ipython 在命令行终端中使用，提供了代码高亮和提示功能, 是mac和linux用户常用的python shell。
![](./images/ipython.png)

### 集成式开发环境选择

#### Sublime 

sublime, 是一款插件式的代码编辑器，可通过安装不同的插件模块来支持不同语言和扩展功能，并且扩平台。

可通过如下步骤安装配置：

1、可以通过官方网站下载安装程序安装Sublime 3或Sublime 2。

2、安装包管理工具。通过快捷键Ctrl+`或者在View菜单中选择Show Console打开控制台，输入下面的代码。

```python
# Sublime 3
import  urllib.request,os;pf='Package Control.sublime-package';ipp=sublime.installed_packages_path();urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler()));open(os.path.join(ipp,pf),'wb').write(urllib.request.urlopen('http://sublime.wbond.net/'+pf.replace(' ','%20')).read())
# Sublime 2
import  urllib2,os;pf='Package Control.sublime-package';ipp=sublime.installed_packages_path();os.makedirs(ipp)ifnotos.path.exists(ipp)elseNone;urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler()));open(os.path.join(ipp,pf),'wb').write(urllib2.urlopen('http://sublime.wbond.net/'+pf.replace(' ','%20')).read());print('Please restart Sublime Text to finish installation')
``` 

- 安装插件。通过Preference菜单的Package Control或快捷键Ctrl+Shift+P打开命令面板，在面板中输入Install Package就可以找到安装插件的工具，然后再查找需要的插件。我们推荐大家安装以下几个插件。

``` 
SublimeCodeIntel - 代码自动补全工具插件
Emmet - 前端开发代码模板插件
Git - 版本控制工具插件
Python PEP8 Autoformat - PEP8规范自动格式化插件
ConvertToUTF8 - 将本地编码转换为UTF-8
```
#### VSCode 

VSCode 是微软公司出的一款轻量级插件式代码编辑工具。它类似sublime也是可以通过安装插件模块来扩展，它也是扩平台的。

相比于Sublime VSCode 自带部分代码开发必须的插件，如git、debug工具和命令行工具等。

对于不喜欢折腾插件，且喜欢轻量级IDE的用户来说，VSCode是最佳选择了。

#### PyCharm

JetBrains 公司推出的标榜 Eclipse的跨平台的 python 集成开发工具，它带有一整套可以帮助用户在使用Python语言开发时提高其效率的工具，比如调试、语法高亮、Project管理、代码跳转、智能提示、自动完成、单元测试、版本控制。此外，该IDE提供了一些高级功能，以用于支持Django等框架下的专业Web开发。

PyCharm 是收费的，但是有功能阉割的社区版本可供我们学习测试使用，[下载地址](http://www.jetbrains.com/pycharm/download/)。

PyCharm的安装、配置和使用我们在后面会进行介绍。


## 总结

本章主要讲解了：
- 计算机的编程基础知识，包括计算机系统的组成、计算机编码等。
- 在3大系统平台如何安装python
- python 编译器
- python IDE的选择

## 参考

- [http://www.regexlab.com/zh/encoding.htm](http://www.regexlab.com/zh/encoding.htm)
- [字符编码笔记：ASCII，Unicode 和 UTF-8](http://www.ruanyifeng.com/blog/2007/10/ascii_unicode_and_utf-8.html)
- [python 之路，致那些年，我们依然没搞明白的编码](https://www.cnblogs.com/alex3714/articles/7550940.html)
- [从Python开始学编程](https://book.douban.com/subject/26919485/)