---
layout : post
title : javascript 使用记录
category : js
date : 2015-11-27 13:26:00
tags : [js]
---



积累记录了一些js常用的操作，备查：

**1、判断json数据是否还有某个key**

```python
//方法一：
obj["key"] != undefined 
//这种有缺陷，如果这个key定义了，并且就是很2的赋值为undefined，那么这句就会出问题了。 
//方法二：
!("key" in obj)
//方法三： 
obj.hasOwnProperty("key")  
```

**2、js对input的限定**

```javascript
//JS判断只能是数字和小数点
//1.文本框只能输入数字代码(小数点也不能输入)
<input onkeyup="this.value=this.value.replace(/\D/g,'')" onafterpaste="this.value=this.value.replace(/\D/g,'')">
//2.只能输入数字,能输小数点.
<input onkeyup="if(isNaN(value))execCommand('undo')" onafterpaste="if(isNaN(value))execCommand('undo')">
<input name=txt1 onchange="if(/\D/.test(this.value)){alert('只能输入数字');this.value='';}">
//3.数字和小数点方法二
<input type=text t_value="" o_value="" onkeypress="if(!this.value.match(/^[\+\-]?\d*?\.?\d*?$/))this.value=this.t_value;else this.t_value=this.value;if(this.value.match(/^(?:[\+\-]?\d+(?:\.\d+)?)?$/))this.o_value=this.value" onkeyup="if(!this.value.match(/^[\+\-]?\d*?\.?\d*?$/))this.value=this.t_value;else this.t_value=this.value;if(this.value.match(/^(?:[\+\-]?\d+(?:\.\d+)?)?$/))this.o_value=this.value" onblur="if(!this.value.match(/^(?:[\+\-]?\d+(?:\.\d+)?|\.\d*?)?$/))this.value=this.o_value;else{if(this.value.match(/^\.\d+$/))this.value=0+this.value;if(this.value.match(/^\.$/))this.value=0;this.o_value=this.value}">
//4.只能输入字母和汉字
<input onkeyup="value=value.replace(/[\d]/g,'') "onbeforepaste="clipboardData.setData('text',clipboardData.getData('text').replace(/[\d]/g,''))" maxlength=10 name="Numbers">
//5.只能输入英文字母和数字,不能输入中文
<input onkeyup="value=value.replace(/[^\w\.\/]/ig,'')">
//6.只能输入数字和英文<font color="Red">chun</font>
<input onKeyUp="value=value.replace(/[^\d|chun]/g,'')">
//7.小数点后只能有最多两位(数字,中文都可输入),不能输入字母和运算符号:
<input onKeyPress="if((event.keyCode<48 || event.keyCode>57) && event.keyCode!=46 || /\.\d\d$/.test(value))event.returnValue=false">
//8.小数点后只能有最多两位(数字,字母,中文都可输入),可以输入运算符号:
<input onkeyup="this.value=this.value.replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')">
//9.只能是数字和小数点和加减乘際
onkeypress="return event.keyCode>=4&&event.keyCode<=57"
```

**3、select的jquery操作**

```javascript
//元素：
<select class="selector">
<option value='test'>test</option>
</select>

//赋值
 $(".selector").val("pxx");
//获取值
 $(".selector").val();
//获取选中项的text
 $(".selector").find("option:selected").text();
 $('.selector option:selected').text();
```


---

#### 参考：

* [http://blog.csdn.net/nairuohe/article/details/6307367](http://blog.csdn.net/nairuohe/article/details/6307367)
* [http://blog.csdn.net/foart/article/details/6614829](http://blog.csdn.net/foart/article/details/6614829)