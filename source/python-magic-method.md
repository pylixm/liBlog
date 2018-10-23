---
layout : post
title : 【 python 基础系列 】 - python 魔法方法
category : python
date : 2018-02-01
tags : [python, Magic Method]
---

本文参考 pycoder's weekly 的文章，做了下python 魔术方法的使用总结，记录备查。

## 介绍 

魔术方法，英文 Magic Methods。顾名思义，它的使用方式不同于一般python方法的使用，它们的使用显得让人捉摸不透，就像魔法一样。在某些场景下python会隐式的调用相应的魔术方法，来完成对应的功能。我们可以重新这些方法来实现与python内建类型相同的对象，或改变python内建类型的相关行为。

魔术方法，通常以双下划线包围，例如我们最熟悉的 `__init__` 就是一个魔术方法。
<!-- more -->
**扩展：python 下划线**
- 单下划线开头（例：_test）: 为符合编码惯例，通常认为是私有变量，无法使用 `from <模块> import *` 引入，除非在 `__all__`中包含了。类及实例均可访问。
- 双下划线开头，例: __test : 类的私有属性, 只有类及其方法内可以访问。
- 前后双下划线：python 内置函数，如魔法函数 `__init__`


下面分类别记录下python中的魔术方法，方便使用备查。

## 常用魔术方法

### 类初始化 

- `__new__` 类初始化时执行，在 `__init__` 函数之前,它的第一个参数是这个类，其他的参数是用来直接传递给 __init__ 方法。详解，[python文档](https://www.python.org/download/releases/2.2/descrintro/#__new__)

- `__init__` 类的初始化方法。new 和 init 可以理解为构造函数。
- `__del__` 析构器，它不实现语句 del x ，定义的是当一个对象进行垃圾回收时候的行为。

**new vs init**

- `__new__`是用来创建类并返回这个类的实例, 而`__init__`只是将传入的参数来初始化该实例.
- `__new__`在创建一个实例的过程中必定会被调用,但`__init__`就不一定，比如通过pickle.load的方式反序列化一个实例时就不会调用`__init__`。
- `__new__`方法总是需要返回该类的一个实例，而`__init__`不能返回除了None的任何值。

### 类的表现

- `__str__` 定义当 str() 调用的时候的返回值。
- `__repr__` 定义 repr() 被调用的时候的返回值, str() 和 repr() 的主要区别在于 repr() 返回的是机器可读的输出，而 str() 返回的是人类可读的。
- `__unicode__(self)` 定义当 unicode() 调用的时候的返回值, unicode() 和 str() 很相似，但是返回的是unicode字符串
- `__hash__(self)` 定义当 hash() 调用的时候的返回值,它返回一个整形。

### 属性控制访问

- `__getarr__(self, name)` 你可以定义当用户试图获取一个不存在的属性时的行为 这适用于对普通拼写错误的获取和重定向，对获取一些不建议的属性时候给出警告(如果你愿意你也可以计算并且给出一个值)或者处理一个 AttributeError
- `__setatt__(self, name, value)` 定义了你对属性进行赋值和修改操作时的行为, 避免"无限递归"的错误
- `__delattr__(self, name)` 定义了删除属性时的行为
- `__getattribute__(self, name)` 定义了你的属性被访问时的行为，同样要避免"无限递归"的错误。需要提醒的是，最好不要尝试去实现`__getattribute__`,因为很少见到这种做法，而且很容易出bug

### 容器类

- `__len__(self)` 需要返回数值类型，以表示容器的长度。该方法在可变容器和不可变容器中必须实现。
- `__getitem__(self, key)` 当你执行self[key]的时候，调用的就是该方法。该方法在可变容器和不可变容器中也都必须实现。调用的时候,如果key的类型错误，该方法应该抛出TypeError；如果没法返回key对应的数值时,该方法应该抛出ValueError。
- `__setitem__(self, key, value)` 当你执行self[key] = value时，调用的是该方法。
- `__delitem__(self, key)` 当你执行del self[key]的时候，调用的是该方法。
- `__iter__(self)` 该方法需要返回一个迭代器(iterator)。当你执行for x in container: 或者使用iter(container)时，该方法被调用。
- `__reversed__(self)` 如果想要该数据结构被內建函数reversed()支持,就还需要实现该方法。
- `__contains__(self, item)` 如果定义了该方法，那么在执行item in container 或者 item not in container时该方法就会被调用。如果没有定义，那么Python会迭代容器中的元素来一个一个比较，从而决定返回True或者False。
- `__missing__(self, key)` dict字典类型会有该方法，它定义了key如果在容器中找不到时触发的行为。比如d = {'a': 1}, 当你执行d[notexist]时，d.__missing__['notexist']就会被调用。
- `__concat__(self, other) ` 来定义当用其他的来连接两个序列时候的行为, 当 + 操作符被调用时候会返回一个 self 和 other.__concat__ 被调用后的结果产生的新序列。 

### 调用对象 

- `__call__(self, [args...])` 允许一个类的实例像函数一样被调用。在那些类的实例经常改变状态的时候会非常有效。调用这个实例是一种改变这个对象状态的直接和优雅的做法

### 回话管理

- `__enter__(self)` 定义当使用 with 语句的时候会话管理器应该初始块被创建的时候的行为.返回值被 with 语句的目标或者 as 后的名字绑定;
- ` __exit__(self, exception_type, exception_value, traceback)` 定义当一个代码块被执行或者终止后会话管理器应该做什么,它可以被用来处理异常，清除工作或者做一些代码块执行完毕之后的日常工作;如果代码块执行成功， exception_type , exception_value , 和 traceback 将会是 None 。否则的话你可以选择处理这个异常或者是直接交给用户处理。如果你想处理这个异常的话，确认 __exit__ 在所有结束之后会返回 True 。


### 描述器 

描述器对象不能独立存在, 它需要被另一个所有者类所持有。描述器对象可以访问到其拥有者实例的属性，在面向对象编程时，如果一个类的属性有相互依赖的关系时，使用描述器来编写代码可以很巧妙的组织逻辑。
如 Django的ORM中, models.Model中的InterField等字段, 就是通过描述器来实现功能的。

为了构建一个描述器，一个类必须有至少 __get__ 或者 __set__ 其中一个，并且 __delete__ 被实现。
- `__get__(self, instance, owner)` 参数instance是拥有者类的实例。参数owner是拥有者类本身。__get__在其拥有者对其读值的时候调用。
- `__set__(self, instance, value)` 在其拥有者对其进行修改值的时候调用。
- `__delete__(self, instance)` 在其拥有者对其进行删除的时候调用。

## 代码实例 
```python 
# -*- coding:utf-8 -*-
from os.path import join


class FileObject(object):
    """给文件对象进行包装从而确认在删除时文件流关闭"""

    def __init__(self, filepath='', filename='sample.txt'):
        # 读写模式打开一个文件
        self.file = open(join(filepath, filename), 'r+')
        print("打开文件")

    def __del__(self):
        self.file.close()
        del self.file
        print('销毁文件')


class Word(str):
    """存储单词的类，定义比较单词的几种方法"""

    def __new__(cls, word):
        # 注意我们必须要用到__new__方法，因为str是不可变类型
        # 所以我们必须在创建的时候将它初始化
        if ' ' in word:
            print("Value contains spaces. Truncating to first space.")
            word = word[:word.index(' ')]  # 单词是第一个空格之前的所有字符
        return str.__new__(cls, word)

    def __init__(self, word):
        self.word = word

    def __gt__(self, other):
        return len(self) > len(other)

    def __lt__(self, other):
        return len(self) < len(other)

    def __ge__(self, other):
        return len(self) >= len(other)

    def __le__(self, other):
        return len(self) <= len(other)

    def __str__(self):
        print('call str func ')
        return "Word: %s" % self.word

    def __repr__(self):
        print('class repr func')
        return "<Word:%s>" % self.word

    def __unicode__(self):
        print('call unicode')
        return 'Word:%s' % self.word


class MyCounter(object):
    """一个包含计数器的控制权限的类每当值被改变时计数器会加一"""

    def __init__(self, val):
        # 使用 super 因为不是所有的类都有 __dict__ 属性
        super(MyCounter, self).__setattr__('counter', 0)
        super(MyCounter, self).__setattr__('value', val)

    def __getattr__(self, item):
        print('call  getattr ')
        return super(MyCounter, self).__getattr__(item)

    def __getattribute__(self, item):
        print('call getattribute')
        return super(MyCounter, self).__getattribute__(item)

    def __setattr__(self, name, value):
        # self.key = value  # 会隐式的再次调用self.__setattr__ 引起递归
        # self.__dict__[key] = value
        print('call setattr')
        if name == 'value':
            super(MyCounter, self).__setattr__('counter', self.counter + 1)
            # 如果你不想让其他属性被访问的话，那么可以抛出 AttributeError(name) 异常
        super(MyCounter, self).__setattr__(name, value)

    def __delattr__(self, name):
        print('call del attr')
        if name == 'value':
            super(MyCounter, self).__setattr__('counter', self.counter + 1)
        super(MyCounter, self).__delattr__(name)


class Container(object):
    """ 容器基类 """

    def __len__(self):
        return len(self)

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, item):
        pass


class DynamicContainer(Container):
    """ 可变容器 """

    def __delitem__(self, key):
        pass

    def __iter__(self):
        pass

    def __reversed__(self):
        pass

    def __contains__(self):
        pass


class NoDynamicContainer(Container):
    """ 不可变容器 """

    def __iter__(self):
        pass

    def __contains__(self):
        pass


class MyList(Container):
    """ 一个封装了一些附加魔术方法比如 head, tail, init, last, drop, 和take的列表类。 """

    def __init__(self, values=None):
        if values is None:
            self.values = []
        else:
            self.values = values

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        # 如果键的类型或者值无效，列表值将会抛出错误
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __delitem__(self, key):
        del self.values[key]

    def __iter__(self):
        return iter(self.values)

    def __reversed__(self):
        return reversed(self.values)

    def append(self, value):
        self.values.append(value)

    def head(self):
        return self.values[0]

    def tail(self):
        return self.values[1:]

    def init(self):
        # 返回一直到末尾的所有元素
        return self.values[:-1]

    def last(self):
        # 返回末尾元素
        return self.values[-1]

    def drop(self, n):
        # 返回除前n个外的所有元素
        return self.values[n:]

    def take(self, n):
        # 返回前n个元素
        return self.values[:n]


class Entity(object):
    """调用实体来改变实体的位置。"""

    def __init__(self, size, x, y):
        self.x, self.y = x, y
        self.size = size

    def __call__(self, x, y):
        """改变实体的位置"""
        self.x, self.y = x, y


class Closer:
    """通过with语句和一个close方法来关闭一个对象的会话管理器"""

    def __init__(self, obj):
        self.obj = obj

    def __enter__(self):
        print('call enter')
        return self.obj  # bound to target

    def __exit__(self, exception_type, exception_val, trace):
        print(exception_type, exception_val, trace)
        try:
            self.obj.close()
        except AttributeError:  # obj isn't closable
            print('Not closable.')
            return True  # exception handled successfully


class Meter(object):
    """Descriptor for a meter."""

    def __init__(self, value=0.0):
        self.value = float(value)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = float(value)


class Foot(object):
    """Descriptor for a foot."""

    def __get__(self, instance, owner):
        return instance.meter * 3.2808

    def __set__(self, instance, value):
        instance.meter = float(value) / 3.2808


class Distance(object):
    meter = Meter()
    foot = Foot()


if __name__ == '__main__':
    # fileobj = FileObject()
    #
    # foo = Word('foo')
    # bara = Word('bara')
    # print(foo > bara)  # False
    # print(foo < bara)  # True
    # print(str('foo') == str('bar'))  # False 利用了 string 内置魔法函数 __eq__

    # print(str(foo))  # Word: foo
    # print(repr(foo))  # <Word:foo>
    # # print(unicode(foo))  # only in python2

    # inst = MyCounter('Test')
    # inst.value = 'test'
    # print(inst.counter)  # 1
    # print(inst.value)  # test
    # inst.value = 'test1'
    # print(inst.counter)  # 2
    # print(inst.value)  # test1  属性存在,只有__getattribute__调用
    # try:
    #     inst.value2  # 属性不存在, 先调用__getattribute__, 后调用__getattr__
    # except AttributeError:
    #     pass
    # del inst.value  # call del attr

    # mylist = MyList([1, 2, 3, 4, 5, 6])
    # print(mylist.head())
    # print(list(mylist.__reversed__()))

    # entiry = Entity(10, 1, 2)
    # entiry(2, 1)
    # print(entiry.x, entiry.y)  # 2 1

    # with Closer(int(5)) as i:
    #     i += 1
    # print(i)
    # with Closer(open('sample.txt')) as file:
    #     print('file>>>>:', file.read())

    d = Distance()
    print(d.meter, d.foot)  # 0.0, 0.0
    d.meter = 1
    print(d.meter, d.foot)  # 1.0 3.2808
    d.meter = 2
    print(d.meter, d.foot)  # 2.0 6.5616

```

## 魔术方法列表 

魔术方法 | 含义
--- | --
   | 基本的魔法方法
`__new__(cls[, ...])`| 1. __new__ 是在一个对象实例化的时候所调用的第一个方法 2. 它的第一个参数是这个类，其他的参数是用来直接传递给 __init__ 方法；3. __new__ 决定是否要使用该 __init__ 方法，因为 __new__ 可以调用其他类的构造方法或者直接返回别的实例对象来作为本类的实例，如果 __new__ 没有返回实例对象，则 __init__ 不会被调用；4. __new__ 主要是用于继承一个不可变的类型比如一个 tuple 或者 string
`__init__(self[, ...])`| 构造器，当一个实例被创建的时候调用的初始化方法
`__del__(self)`| 析构器，当一个实例被销毁的时候调用的方法
`__call__(self[, args...])`| 允许一个类的实例像函数一样被调用：x(a, b) 调用 x.__call__(a, b)
`__len__(self)`| 定义当被 len() 调用时的行为
`__repr__(self)`| 定义当被 repr() 调用时的行为
`__str__(self)`| 定义当被 str() 调用时的行为
`__bytes__(self)`| 定义当被 bytes() 调用时的行为
`__hash__(self)`| 定义当被 hash() 调用时的行为
`__bool__(self)`| 定义当被 bool() 调用时的行为，应该返回 True 或 False
`__format__(self, format_spec)`| 定义当被 format() 调用时的行为
 | 有关属性
`__getattr__(self, name)`| 定义当用户试图获取一个不存在的属性时的行为
`__getattribute__(self, name)`| 定义当该类的属性被访问时的行为
`__setattr__(self, name, value)`| 定义当一个属性被设置时的行为
`__delattr__(self, name)`| 定义当一个属性被删除时的行为
`__dir__(self)`| 定义当 dir() 被调用时的行为
`__get__(self, instance, owner)`| 定义当描述符的值被取得时的行为
`__set__(self, instance, value)`| 定义当描述符的值被改变时的行为
`__delete__(self, instance)`| 定义当描述符的值被删除时的行为
 | 比较操作符
`__lt__(self, other)`| 定义小于号的行为：x < y 调用 x.__lt__(y)
`__le__(self, other)`| 定义小于等于号的行为：x <= y 调用 x.__le__(y)
`__eq__(self, other)`| 定义等于号的行为：x == y 调用 x.__eq__(y)
`__ne__(self, other)`| 定义不等号的行为：x != y 调用 x.__ne__(y)
`__gt__(self, other)`| 定义大于号的行为：x > y 调用 x.__gt__(y)
`__ge__(self, other)`| 定义大于等于号的行为：x >= y 调用 x.__ge__(y)
 | 算数运算符
`__add__(self, other)`| 定义加法的行为：+
`__sub__(self, other)`| 定义减法的行为：-
`__mul__(self, other)`| 定义乘法的行为：*
`__truediv__(self, other)`| 定义真除法的行为：/
`__floordiv__(self, other)`| 定义整数除法的行为：//
`__mod__(self, other)`| 定义取模算法的行为：%
`__divmod__(self, other)`| 定义当被 divmod() 调用时的行为
`__pow__(self, other[, modulo])`| 定义当被 power() 调用或 ** 运算时的行为
`__lshift__(self, other)`| 定义按位左移位的行为：<<
`__rshift__(self, other)`| 定义按位右移位的行为：>>
`__and__(self, other)`| 定义按位与操作的行为：&
`__xor__(self, other)`| 定义按位异或操作的行为：^
`__or__(self, other)`| 定义按位或操作的行为：|
 | 反运算
`__radd__(self, other)`| （与上方相同，当左操作数不支持相应的操作时被调用）
`__rsub__(self, other)`| （与上方相同，当左操作数不支持相应的操作时被调用）
`__rmul__(self, other)`| （与上方相同，当左操作数不支持相应的操作时被调用）
`__rtruediv__(self, other)`| （与上方相同，当左操作数不支持相应的操作时被调用）
`__rfloordiv__(self, other)`| （与上方相同，当左操作数不支持相应的操作时被调用）
`__rmod__(self, other)`| （与上方相同，当左操作数不支持相应的操作时被调用）
`__rdivmod__(self, other)`| （与上方相同，当左操作数不支持相应的操作时被调用）
`__rpow__(self, other)`| （与上方相同，当左操作数不支持相应的操作时被调用）
`__rlshift__(self, other)`| （与上方相同，当左操作数不支持相应的操作时被调用）
`__rrshift__(self, other)`| （与上方相同，当左操作数不支持相应的操作时被调用）
`__rxor__(self, other)`| （与上方相同，当左操作数不支持相应的操作时被调用）
`__ror__(self, other)`| （与上方相同，当左操作数不支持相应的操作时被调用）
 | 增量赋值运算
`__iadd__(self, other)`| 定义赋值加法的行为：+=
`__isub__(self, other)`| 定义赋值减法的行为：-=
`__imul__(self, other)`| 定义赋值乘法的行为：*=
`__itruediv__(self, other)`| 定义赋值真除法的行为：/=
`__ifloordiv__(self, other)`| 定义赋值整数除法的行为：//=
`__imod__(self, other)`| 定义赋值取模算法的行为：%=
`__ipow__(self, other[, modulo])`| 定义赋值幂运算的行为：**=
`__ilshift__(self, other)`| 定义赋值按位左移位的行为：<<=
`__irshift__(self, other)`| 定义赋值按位右移位的行为：>>=
`__iand__(self, other)`| 定义赋值按位与操作的行为：&=
`__ixor__(self, other)`| 定义赋值按位异或操作的行为：^=
`__ior__(self, other)`| 定义赋值按位或操作的行为：|=
 | 一元操作符
`__neg__(self)`| 定义正号的行为：+x
`__pos__(self)`| 定义负号的行为：-x
`__abs__(self)`| 定义当被 abs() 调用时的行为
`__invert__(self)`| 定义按位求反的行为：~x
 | 类型转换
`__complex__(self)`| 定义当被 complex() 调用时的行为（需要返回恰当的值）
`__int__(self)`| 定义当被 int() 调用时的行为（需要返回恰当的值）
`__float__(self)`| 定义当被 float() 调用时的行为（需要返回恰当的值）
`__round__(self[, n])`| 定义当被 round() 调用时的行为（需要返回恰当的值）
`__index__(self)`| 1. 当对象是被应用在切片表达式中时，实现整形强制转换；2. 如果你定义了一个可能在切片时用到的定制的数值型,你应该定义 __index__；3. 如果 __index__ 被定义，则 __int__ 也需要被定义，且返回相同的值
 | 上下文管理（with 语句）
`__enter__(self)`| 1. 定义当使用 with 语句时的初始化行为；2. __enter__ 的返回值被 with 语句的目标或者 as 后的名字绑定
`__exit__(self, exc_type, exc_value, traceback)`| 1. 定义当一个代码块被执行或者终止后上下文管理器应该做什么；2. 一般被用来处理异常，清除工作或者做一些代码块执行完毕之后的日常工作
 | 容器类型
`__len__(self)`| 定义当被 len() 调用时的行为（返回容器中元素的个数）
`__getitem__(self, key)`| 定义获取容器中指定元素的行为，相当于 self[key]
`__setitem__(self, key, value)`| 定义设置容器中指定元素的行为，相当于 self[key] = value
`__delitem__(self, key)`| 定义删除容器中指定元素的行为，相当于 del self[key]
`__iter__(self)`| 定义当迭代容器中的元素的行为
`__reversed__(self)`| 定义当被 reversed() 调用时的行为
`__contains__(self, item)`| 定义当使用成员测试运算符（in 或 not in）时的行为


## 延伸阅读
- [Dive into Python3:Special Method Names](http://www.diveintopython3.net/special-method-names.html)

## 参考

- [Python 魔术方法指南](http://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/a-guide-to-pythons-magic-methods.html#id22)

