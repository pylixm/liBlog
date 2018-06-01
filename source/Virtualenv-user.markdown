---
layout : post
title : 使用virtualenv 部署django应用问题记录
category : vcs
date : 2016-01-18 19:50:00
tags : [virtualenv,]
---


使用virtualenv来部署django应用，大大缩减了我们搭建环境的时间。初次使用，以为创建好的env可以直接复制使用。实际使用时，确遇到了各种问题。

env在不同环境下使用，还是需要简单修改配置的。今天测试了下，必须确保如下几点，才可使用：

- 确保env 的存放路径和 activate 中 `VIRTUAL_ENV` 路径一致。

- 确保python 的版本及安装路径一致。因为，env环境 lib 中的python 库是指向实际python库的链接，并非真正的库文件。






