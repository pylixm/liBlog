---
layout : post
title : Django学习笔记-模板
category : django
date : 2015-11-15 16:30:00
tags : [django,]
---



### 语法

#### 变量

双括号
    
#### 判断
   
使用大括号+%
if xx 
 xx  
else
 xx 
endif 
 
ifequal athlete.name coach.name 
 xx
else
 xx 
endifequal 

for athlete in athlete_list
 xx
endfor

for key, value in data.items
endfor
<!-- more -->    
#### 循环中使用的变量

`forloop.counter` 总是一个表示当前循环的执行次数的整数计数器。 
这个计数器是从1开始的，所以在第一次循环时 forloop.counter 将会被设置为1。

`forloop.counter0` 类似于 forloop.counter ，但是它是从0计数的。 第一次执行循环时这个变量会被设置为0。

`forloop.revcounter` 是表示循环中剩余项的整型变量。 在循环初次执行时 forloop.revcounter 将被设置为序列中项的总数。 最后一次循环执行中，这个变量将被置1。

`forloop.revcounter0` 类似于 forloop.revcounter ，但它以0做为结束索引。在第一次执行循环时，该变量会被置为序列的项的个数减1。

`forloop.first` 是一个布尔值。 在第一次执行循环时该变量为True。

`forloop.last` 是一个布尔值；在最后一次执行循环时被置为True。一个常见的用法是在一系列的链接之间放置管道符（|）
另一个常见的用途是为列表的每个单词的加上逗号。

`forloop.parentloop` 是一个指向当前循环的上一级循环的 forloop 对象的引用（在嵌套循环的情况下）。 


#### 模板过滤器

**数字过滤器**

`apnumber` 对于 1 到 9 的数字，该过滤器返回了数字的拼写形式。 否则，它将返回数字。 这遵循的是美联社风格。

`intcomma` 该过滤器将整数转换为每三个数字用一个逗号分隔的字符串。

`intword` 该过滤器将一个很大的整数转换成友好的文本表示方式。 它对于超过一百万的数字最好用。
最大支持不超过一千的五次方（1,000,000,000,000,000）。

`ordinal` 该过滤器将整数转换为序数词的字符串形式。

**时间过滤器**

`date` date:"Y-m-d H:i:s"
 
**其他**

`lower` 小写

`my_text|escape|linebreaks ` 串联：先转义文本到HTML，再转换每行到 <p> 标签

`bio | truncatewords:"30" ` 显示前30个字
 
`123|add:"5" ` 给value加上一个数值

`"AB'CD"|addslashes `单引号加上转义号，一般用于输出到javascript中

`"abcd"|capfirst ` 第一个字母大写

`"abcd"|center:"50" ` 输出指定长度的字符串，并把值对中

`"123spam456spam789"|cut:"spam" ` 查找删除指定字符串

`value|date:"F j, Y" ` 格式化日期

`value|default:"(N/A)" ` 值不存在，使用指定值

`value|default_if_none:"(N/A)" ` 值是None，使用指定值

`列表变量|dictsort:"数字" ` 排序从小到大

`列表变量|dictsortreversed:"数字" ` 排序从大到小

`if 92|divisibleby:"2" ` 判断是否整除指定数字

` string|escape` 转换为html实体

` 21984124|filesizeformat` 以1024为基数，计算最大值，保留1位小数，增加可读性

` list|first` 返回列表第一个元素

` "ik23hr&jqwh"|fix_ampersands` &转为&amp;

` 13.414121241|floatformat ` 保留1位小数，可为负数，几种形式

` 13.414121241|floatformat:"2" ` 保留2位小数

` 23456 |get_digit:"1" ` 从个位数开始截取指定位置的1个数字

``list|join:", " ` 用指定分隔符连接列表

`list|length ` 返回列表个数

`if 列表|length_is:"3" ` 列表个数是否指定数值

`"ABCD"|linebreaks ` 用新行用<p> 、 <br /> 标记包裹

`"ABCD"|linebreaksbr ` 用新行用<br /> 标记包裹

`变量|linenumbers ` 为变量中每一行加上行号

`"abcd"|ljust:"50" ` 把字符串在指定宽度中对左，其它用空格填充

`for i in "1abc1"|make_list` 把字符串或数字的字符个数作为一个列表

`"abcdefghijklmnopqrstuvwxyz"|phone2numeric ` 把字符转为可以对应的数字？？

`列表或数字|pluralize `单词的复数形式，如列表字符串个数大于1，返回s，否则返回空串

`列表或数字|pluralize:"es"` 指定es

`列表或数字|pluralize:"y,ies" ` 指定ies替换为y

`object|pprint ` 显示一个对象的值

`列表|random ` 返回列表的随机一项

`string|removetags:"br p div" ` 删除字符串中指定html标记

`string|rjust:"50" ` 把字符串在指定宽度中对右，其它用空格填充

`` 列表|slice:":2" ` 切片

` string|slugify ` 字符串中留下减号和下划线，其它符号删除，空格用减号替换

` 3|stringformat:"02i" `字符串格式，使用Python的字符串格式语法

` "E<A>A</A>B<C>C</C>D"|striptags ` 剥去[X]HTML语法标记

` 时间变量|time:"P" ` 日期的时间部分格式

` datetime|timesince ` 给定日期到现在过去了多少时间

` datetime|timesince:"other_datetime" ` 两日期间过去了多少时间


` datetime|timeuntil ` 给定日期到现在过去了多少时间，与上面的区别在于2日期的前后位置。

` datetime|timeuntil:"other_datetime" ` 两日期间过去了多少时间

` "abdsadf"|title ` 首字母大写

` "A B C D E F"|truncatewords:"3" ` 截取指定个数的单词

` "<a>1<a>1<a>1</a></a></a>22<a>1</a>"|truncatewords_html:"2" ` 截取指定个数的html标记，并补完整

`list|unordered_list ` 多重嵌套列表展现为html的无序列表

` string|upper ` 全部大写

`link|urlencode` url编码

` string|urlize ` 将URLs由纯文本变为可点击的链接。（没有实验成功）

` string|urlizetrunc:"30"` 同上，多个截取字符数。（同样没有实验成功）

` "B C D E F"|wordcount ` 单词数

` "a b c d e f g h i j k"|wordwrap:"5" `每指定数量的字符就插入回车符

` boolean|yesno:"Yes,No,Perhaps" ` 对三种值的返回字符串，对应是 非空,空,None

