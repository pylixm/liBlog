---
layout : post
title : Linux基础系列 - jq
category : linux
date : 2018-06-26
tags : [linux, linux基础系列, 运维知识库]
---

## 介绍 

`jq` 是linux下的一个解析JSON格式字符串的一个命令行工具。可直接使用 `yum install jq` 来安装。
<!-- more -->
```bash
jq - commandline JSON processor [version 1.5]
Usage: jq [options] <jq filter> [file...]

	jq is a tool for processing JSON inputs, applying the
	given filter to its JSON text inputs and producing the
	filter's results as JSON on standard output.
	The simplest filter is ., which is the identity filter,
	copying jq's input to its output unmodified (except for
	formatting).
	For more advanced filters see the jq(1) manpage ("man jq")
	and/or https://stedolan.github.io/jq

	Some of the options include:
	 -c		compact instead of pretty-printed output;
	 -n		use `null` as the single input value;
	 -e		set the exit status code based on the output;
	 -s		read (slurp) all inputs into an array; apply filter to it;
	 -r		output raw strings, not JSON texts;
	 -R		read raw strings, not JSON texts;
	 -C		colorize JSON;
	 -M		monochrome (don't colorize JSON);
	 -S		sort keys of objects on output;
	 --tab	use tabs for indentation;
	 --arg a v	set variable $a to value <v>;
	 --argjson a v	set variable $a to JSON value <v>;
	 --slurpfile a f	set variable $a to an array of JSON texts read from <f>;
	See the manpage for more options.
```

## 使用 

### 格式化 

```bash 
[root@pylixm-web ~]# cat test.txt
{"name":"Google","location":{"street":"1600 Amphitheatre Parkway","city":"Mountain View","state":"California","country":"US"},"employees":[{"name":"Michael","division":"Engineering"},{"name":"Laura","division":"HR"},{"name":"Elise","division":"Marketing"}]}
```

直接格式化，并校验合法性：

```bash
[root@pylixm-web ~]# cat test.txt |jq .
{
  "name": "Google",
  "location": {
    "street": "1600 Amphitheatre Parkway",
    "city": "Mountain View",
    "state": "California",
    "country": "US"
  },
  "employees": [
    {
      "name": "Michael",
      "division": "Engineering"
    },
    {
      "name": "Laura",
      "division": "HR"
    },
    {
      "name": "Elise",
      "division": "Marketing"
    }
  ]
}
```

### 解析 

**可直接通过key获取到JSON的value**

```bash
[root@pylixm-web ~]# cat test.txt |jq .name
"Google"
[root@pylixm-web ~]# cat test.txt |jq .test
null
```

当key不存在时，会返回`null`。

**嵌套解析**

```bash
[root@pylixm-web ~]# cat test.txt |jq .location.city
"Mountain View"
[root@pylixm-web ~]# cat test.txt |jq .employees[]
{
  "name": "Michael",
  "division": "Engineering"
}
{
  "name": "Laura",
  "division": "HR"
}
{
  "name": "Elise",
  "division": "Marketing"
}
[root@pylixm-web ~]# cat test.txt |jq .employees[0]
{
  "name": "Michael",
  "division": "Engineering"
}
[root@pylixm-web ~]# cat test.txt |jq .employees[0].name
"Michael"
```

可使用key 连续获取嵌套的json数据。当值为数组时，可通过下标来获取对应位置的json数据。

### 内建函数

**keys**

获取最外层的关键字keys，返回一个数组。只能在最外层使用。

```bash
[root@pylixm-web ~]# cat test.txt |jq keys
[
  "employees",
  "location",
  "name"
]
[root@pylixm-web ~]# cat test.txt |jq .location.keys
null
```

**has**

判断是否含有某个key，返回一个布尔值的字符串类型。

```bash
[root@pylixm-web ~]# cat test.txt |jq 'has("test")'
false
```


## 参考 

- [https://blog.csdn.net/yanbingquan/article/details/50770911](https://blog.csdn.net/yanbingquan/article/details/50770911)