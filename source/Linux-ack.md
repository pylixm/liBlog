---
layout : post
title : Linux基础系列 - 三剑客之 ack 命令使用总结
category : linux
date : 2018-10-16
tags : [linux, linux基础系列, 运维知识库]
---

## 简介

`awk` 是在linux环境下，分析文本的一个利器，与`grep`、`sed`被称为linux三剑客。`awk`功能强大，可以进行正则表达式的匹配，样式装入、流控制、数学运算符、进程控制语句甚至于内置的变量和函数。它具备了一个完整的语言所应具有的几乎所有精美特性。`awk`其名称得自于它的创始人 Alfred Aho 、Peter Weinberger 和 Brian Kernighan 姓氏的首个字母。实际上 AWK 的确拥有自己的语言： AWK 程序设计语言 ， 三位创建者已将它正式定义为“样式扫描和处理语言”。
<!-- more -->

## 使用方发

### 基本语法结构

```
语法：
awk [options] 'script' var=value file(s)
awk [options] -f scriptfile var=value file(s)
```

常用参数：
- -F fs   fs指定输入分隔符，fs可以是字符串或正则表达式，如-F:
- -v var=value   赋值一个用户定义变量，将外部变量传递给awk
- -f scripfile  从脚本文件中读取awk命令


awk 的基本结构如下：

```
# awk 'BEGIN{ commands } pattern{ commands } END{ commands }'
awk 'BEGIN{ print 'Start>>>' } ~/mysql/{ print $0 } END{ print "End" }' test.txt
awk '{print $0}' test.txt 
```
说明：
- BEGIN语句块在awk开始从输入流中读取行之前被执行，这是一个可选的语句块，比如变量初始化、打印输出表格的表头等语句通常可以写在BEGIN语句块中。
- END语句块在awk从输入流中读取完所有的行之后即被执行，比如打印所有行的分析结果这类信息汇总都是在END语句块中完成，它也是一个可选语句块。
- pattern语句块中的通用命令是最重要的部分，它也是可选的。如果没有提供pattern语句块，则默认执行{ print }，即打印每一个读取到的行，awk读取的每一行都会执行该语句块。
- $0 为一个内置变量。
- /mysql/ 为正则表达式。
- ~ 表示模式开启。

执行过程如下：
- 第一步：执行BEGIN{ commands }语句块中的语句；
- 第二步：从文件或标准输入(stdin)读取一行，然后执行pattern{ commands }语句块，它逐行扫描文件，从第一行到最后一行重复这个过程，直到文件全部被读取完毕。
- 第三步：当读至输入流末尾时，执行END{ commands }语句块。

### 内置变量

awk 有些内置的变量，我们可以直接调用来使用：

```
说明：[A][N][P][G]表示第一个支持变量的工具，[A]=awk、[N]=nawk、[P]=POSIXawk、[G]=gawk，nawk/POSIXawk/gawk均为awk的扩展版本。
$n 当前记录的第n个字段，比如n为1表示第一个字段，n为2表示第二个字段。 
$0 这个变量包含执行过程中当前行的文本内容。
[N] ARGC 命令行参数的数目。
[G] ARGIND 命令行中当前文件的位置（从0开始算）。
[N] ARGV 包含命令行参数的数组。
[G] CONVFMT 数字转换格式（默认值为%.6g）。
[P] ENVIRON 环境变量关联数组。
[N] ERRNO 最后一个系统错误的描述。
[G] FIELDWIDTHS 字段宽度列表（用空格键分隔）。
[A] FILENAME 当前输入文件的名。
[P] FNR 同NR，但相对于当前文件。
[A] FS Begin中定义字段分隔符（默认是任何空格）。
[G] IGNORECASE 如果为真，则进行忽略大小写的匹配。
[A] NF 表示字段数，在执行过程中对应于当前的字段数。
[A] NR 表示记录数，在执行过程中对应于当前的行号。
[A] OFMT 数字的输出格式（默认值是%.6g）。
[A] OFS 输出字段分隔符（默认值是一个空格）。
[A] ORS 输出记录分隔符（默认值是一个换行符）。
[A] RS 记录分隔符（默认是一个换行符）。
[N] RSTART 由match函数所匹配的字符串的第一个位置。
[N] RLENGTH 由match函数所匹配的字符串的长度。
[N] SUBSEP 数组下标分隔符（默认值是34）。
```

这些变量我们再处理文本是可直接使用。例如，我要获取每行文本的最后一个字段，我就可以这样写：

```
awk '{print $NF}'
```

### 参数

**-F**

默认awk会将每行文本字符按空格来分成若干字段再来进一步处理，可以使用此参数来自定义awk的行分割符号。

实例，

```
awk -F "." test.txt 
```

**-v**

可以将外部值（并非来自stdin）传递给awk。

```shell
VAR=10000
echo | awk -v VARIABLE=$VAR '{ print VARIABLE }'
```

```shell
# 其他赋值
var1="aaa"
var2="bbb"
echo | awk '{ print v1,v2 }' v1=$var1 v2=$var2

# 从文件中获取变量
awk '{ print v1,v2 }' v1=$var1 v2=$var2 filename
```

**-f**

awk 命令可写入文件，通过此参数调用。

```shell
# cal.awk 
{print $0}

# 通过文件调用
awk -f cal.awk test.txt
```

### 运算

**条件表达式**
==   !=   >   >=  
awk -F":" '$1=="mysql"{print $3}' /etc/passwd  
awk -F":" '{if($1=="mysql") print $3}' /etc/passwd          //与上面相同 
awk -F":" '$1!="mysql"{print $3}' /etc/passwd                 //不等于
awk -F":" '$3>1000{print $3}' /etc/passwd                      //大于
awk -F":" '$3>=100{print $3}' /etc/passwd                     //大于等于
awk -F":" '$3<1{print $3}' /etc/passwd                            //小于
awk -F":" '$3<=1{print $3}' /etc/passwd                         //小于等于

**逻辑运算符**
&&　|| 
awk -F: '$1~/mail/ && $3>8 {print }' /etc/passwd         //逻辑与，$1匹配mail，并且$3>8
awk -F: '{if($1~/mail/ && $3>8) print }' /etc/passwd
awk -F: '$1~/mail/ || $3>1000 {print }' /etc/passwd       //逻辑或
awk -F: '{if($1~/mail/ || $3>1000) print }' /etc/passwd 
 
**数值运算**
awk -F: '$3 > 100' /etc/passwd    
awk -F: '$3 > 100 || $3 < 5' /etc/passwd  
awk -F: '$3+$4 > 200' /etc/passwd
awk -F: '/mysql|mail/{print $3+10}' /etc/passwd                    //第三个字段加10打印 
awk -F: '/mysql/{print $3-$4}' /etc/passwd                             //减法
awk -F: '/mysql/{print $3*$4}' /etc/passwd                             //求乘积
awk '/MemFree/{print $2/1024}' /proc/meminfo                  //除法
awk '/MemFree/{print int($2/1024)}' /proc/meminfo           //取整


###  控制语句


**IF语句**
必须用在{}中，且比较内容用()扩起来
awk -F: '{if($1~/mail/) print $1}' /etc/passwd                                       //简写
awk -F: '{if($1~/mail/) {print $1}}'  /etc/passwd                                   //全写
awk -F: '{if($1~/mail/) {print $1} else {print $2}}' /etc/passwd            //if...else...

**while语句**
awk -F: 'BEGIN{i=1} {while(i<NF) print NF,$i,i++}' /etc/passwd 

**for语句**

seq 9 | sed 'H;g' | awk -v RS='' '{for(i=1;i<=NF;i++)printf("%dx%d=%d%s", i, NR, i*NR, i==NR?"\n":"\t")}' 


## 常用总结

### IP相关统计

```shell
#统计IP访问量（独立ip访问数量）
awk '{print $1}' access.log | sort -n | uniq | wc -l

# 查看某一时间段的IP访问量(4-5点)
grep "07/Apr/2017:0[4-5]" access.log | awk '{print $1}' | sort | uniq -c| sort -nr | wc -l  

# 查看访问最频繁的前100个IP
awk '{print $1}' access.log | sort -n |uniq -c | sort -rn | head -n 100

# 查看访问100次以上的IP
awk '{print $1}' access.log | sort -n |uniq -c |awk '{if($1 >100) print $0}'|sort -rn
# 查询某个IP的详细访问情况,按访问频率排序
grep '127.0.01' access.log |awk '{print $7}'|sort |uniq -c |sort -rn |head -n 100
```

### 页面访问统计

```shell

# 查看访问最频的页面(TOP100)
awk '{print $7}' access.log | sort |uniq -c | sort -rn | head -n 100

# 查看访问最频的页面([排除php页面】(TOP100)
grep -v ".php"  access.log | awk '{print $7}' | sort |uniq -c | sort -rn | head -n 100 

# 查看页面访问次数超过100次的页面
cat access.log | cut -d ' ' -f 7 | sort |uniq -c | awk '{if ($1 > 100) print $0}' | less

# 查看最近1000条记录，访问量最高的页面
tail -1000 access.log |awk '{print $7}'|sort|uniq -c|sort -nr|less
```

### 请求量统计

```shell
# 统计每秒的请求数,top100的时间点(精确到秒)
awk '{print $4}' access.log |cut -c 14-21|sort|uniq -c|sort -nr|head -n 100

# 统计每分钟的请求数,top100的时间点(精确到分钟)
awk '{print $4}' access.log |cut -c 14-18|sort|uniq -c|sort -nr|head -n 100

# 统计每小时的请求数,top100的时间点(精确到小时)
awk '{print $4}' access.log |cut -c 14-15|sort|uniq -c|sort -nr|head -n 100
```

### 性能分析

在nginx log中最后一个字段加入$request_time

```shell
# 列出传输时间超过 3 秒的页面，显示前20条
cat access.log|awk '($NF > 3){print $7}'|sort -n|uniq -c|sort -nr|head -20

# 列出php页面请求时间超过3秒的页面，并统计其出现的次数，显示前100条
cat access.log|awk '($NF > 1 &&  $7~/\.php/){print $7}'|sort -n|uniq -c|sort -nr|head -100
```

### 蜘蛛抓取统计

```shell
# 统计蜘蛛抓取次数
grep 'Baiduspider' access.log |wc -l

# 统计蜘蛛抓取404的次数
grep 'Baiduspider' access.log |grep '404' | wc -l
```

### TCP连接统计

```shell
# 查看当前TCP连接数
netstat -tan | grep "ESTABLISHED" | grep ":80" | wc -l

# 用tcpdump嗅探80端口的访问看看谁最高
tcpdump -i eth0 -tnn dst port 80 -c 1000 | awk -F"." '{print $1"."$2"."$3"."$4}' | sort | uniq -c | sort -nr
```

## 参考

- [http://man.linuxde.net/awk#%E8%B5%8B%E5%80%BC%E8%BF%90%E7%AE%97%E7%AC%A6](http://man.linuxde.net/awk#%E8%B5%8B%E5%80%BC%E8%BF%90%E7%AE%97%E7%AC%A6)
- [http://blog.chinaunix.net/uid-23302288-id-3785105.html](http://blog.chinaunix.net/uid-23302288-id-3785105.html)