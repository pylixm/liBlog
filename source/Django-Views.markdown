---
layout : post
title : Django学习笔记-url、视图
category : django
date : 2015-11-15 16:00:00
tags : [django,]
---


## 路由(URL)

Django中有个指定url和视图函数的 urlconf 文件，组成如下：

- 一个打头的前缀字符串，可以为空。
- 一个或多个由正则表达式字符串匹配一个或一组URL组成的python元组；一个视图函数对象或字符串；有时还可以带上一个视图函数的字典参数。

<!-- more -->
例：

```python
urlpatterns = patterns('',
	# Examples:
	#'^$' 表示为web的根目录，Django会自动去除url前的 / 
	# 'djdemo02.views.home' ,对应的视图函数
	# name 他必须在所有的url里唯一，可以在别的地方通过 name 来引用此url
	(r'^$', 'djdemo02.views.home', name='home'),
	url(r'^$', 'djdemo02.views.home', name='home'),
)
urlpatterns += patterns(
	url(r'^admin/', include(admin.site.urls)),
	url(r'blog/',include('blog.urls')),
)
```

注：

1. 多个patterns 可以使用 += 链接 ；
2. 可以使用 include('blog.urls') 函数来包含其他的url文件 ；
3. 动态url使用圆括号把参数在URL模式里标识 出来；

例：

```python
(r'^time/plus/(\d{1,2})/$', hours_ahead),
```

## HTTP

所有视图均接受一个来自前台的 HttpRequest对象 
HttpRequest对象属性， 均为键值对 。

**GET、POST、REQUEST**

```python
GET #接受get请求的参数 
POST #接收 post请求参数
REQUEST #均可；
```

**Cookies 、 Sessions**

```python
#注意这俩各属性的大小写
request.COOKIES 
request.session
```

**其他属性**

只读

- ``path``：url里域名后的部分
- ``method``：返回http的请求方法
- ``encoding`` :标明了用来解码表单的字符集
- ``FILES``：包含了通过文件输入表单字段上传的文件 
- ``META``：它包含了所有没有被请求的其他部分处理的HTTP服务器请求变量。
- ``user``: django的认证用户，只有你的站点激活django认证机制才有；
- ``raw_post_data``: 请求里包含的POST原始数据。比POST更全。
    
## HTTPResponse对象

构建方法

	1、response = HttpResponse("<html>Hello word!</html>")
	2、response = HttpResponse()
	   response.write("<html>")
	   response.write("Hello word!")
	   response.write("</html>")
	3、设置http头，
	    response = HttpResponse()
	    response["Content-Type"] = "text/csv"
	    response["Content-Length"] = 256

## 中间件

    是一些python函数可以在上述过程里的多个地方执行来改变真个应用程序的输入（在请求到达视图之前对他进行修改）
    输出（修改视图创建的响应）
   

## 视图和逻辑

### 通用视图 
	todo

### 自定义视图

    todo
    
[模板篇](/Django-Tempalete.md)


#### 参考

