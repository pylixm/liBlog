---
layout : post
title : Vue.js 初尝试
category : js
date : 2016-11-16 
tags : [js, vue]
---

最近看了阮一峰的全站培训教材[这里](https://github.com/ruanyf/jstraining)，感叹现如今前端发展之迅猛。

今天特尝试了下 Vue（2.0） 框架，记录如下备查。


### 一、基本概念

#### 1.1 Vue

Vue.js 。它提供了 MVVM 数据绑定和一个可组合的组件系统，具有简单、灵活的 API。

从技术上讲， Vue.js 集中在 MVVM 模式上的视图模型层，并通过双向数据绑定连接视图和模型。实际的 DOM 操作和输出格式被抽象出来成指令和过滤器。
相比其它的 MVVM 框架，Vue.js 更容易上手。

#### 1.2 MVVM 概念

相比与后端的MVC 框架
- Model：管理数据
- View：数据的展现
- View-Model：简化的 Controller，唯一作用就是为 View 提供处理好的数据，不含其他逻辑。

本质：view 绑定 view-model，视图与数据模型强耦合。数据的变化实时反映在 view 上，不需要手动处理。

![](/static/imgs/mvvm.png)
(图片来源：[阮一峰培训教材](https://github.com/ruanyf/jstraining/blob/master/docs/images/mvvm.png))

### 二、基本使用

#### 2.1 数据绑定 

``\{\{\}\}`` 来渲染字符串、表达式等
``v-bind`` 对于html属性值的渲染 缩写 `:`
``\{\{ message | capitalize \}\}`` 可使用过滤器，过滤器可串联，可传参。

参考事例：
```html 
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://unpkg.com/vue/dist/vue.js"></script>
  <title>vue实例</title>
</head>
  <body>
    <div id="app">
      {{ message }}
    </div>
    <div id="app-2">
      <span v-bind:title="message">
        Hover your mouse over me for a few seconds to see my dynamically bound title!
      </span>
    </div>

  <script type="text/javascript">
   //简单渲染
    var app = new Vue({
      el: '#app',
      data: {
        message: 'Hello Vue!'
      }
    })
    //指令方式渲染
    var app2 = new Vue({
      el: '#app-2',
      data: {
        message: 'You loaded this page on ' + new Date()
      }
    })
  </script>
  </body>
  </html>

```

此时页面显示如下：

![](/static/imgs/sjbd.png)

动态的修改js中元素的值，可以动态的显示到Dom元素中。实现了数据绑定，这样我们就可以省去使用js来替换html元素中内容之类的操作了。

#### 2.2 DOM绑定

`v-if` `v-else` 来进行条件渲染，除了数据可对DOM进行绑定。
`v-for` 进行循环渲染，可对列表和字典数据做遍历。

参考实例：
```html
    <!--条件/循环-->
    <div id="app-3">
      <p v-if="seen">Now you see me</p>
      <p v-else>I am else </p>
    </div>
    <div id="app-4">
      <ol>
        <li v-for="todo in todos">
          {{ todo.text }}
        </li>
      </ol>
      <div v-for="(value, key, index) in object">
       {{ index }}. {{ key }} : {{ value }}
      </div>
    </div>

    <script>
        var app3 = new Vue({
      el: '#app-3',
      data: {
        seen: true
      }
    })
    var app4 = new Vue({
      el: '#app-4',
      data: {
        todos: [
          { text: 'Learn JavaScript' },
          { text: 'Learn Vue' },
          { text: 'Build something awesome' }
        ]
      }
    })
    </script>
```
#### 2.3 事件绑定

`v-on` 进行事件绑定，缩写 `@`


```html
<div id="example-1">
  <button v-on:click="counter += 1">增加 1</button>
  <p>这个按钮被点击了 {{ counter }} 次。</p>
</div>
//按键修饰符
<input v-on:keyup.enter="submit">
<!-- 缩写语法 -->
<input @keyup.enter="submit">
<!--
全部的按键别名：
- enter
- tab
- delete (捕获 “删除” 和 “退格” 键)
- esc
- space
- up
- down
- left
- right
-->
```

#### 2.4 表单控件绑定

`v-model` 来绑定表单控件

```html
<!--文本-->
<input v-model="message" placeholder="edit me">
<p>Message is: {{ message }}</p>
<!--多文本-->
<span>Multiline message is:</span>
<p style="white-space: pre">{{ message }}</p>
<br>
<textarea v-model="message" placeholder="add multiple lines"></textarea>
<!--复选-->
<input type="checkbox" id="checkbox" v-model="checked">
<label for="checkbox">{{ checked }}</label>
<!--单选-->
<input type="radio" id="one" value="One" v-model="picked">
<label for="one">One</label>
<br>
<input type="radio" id="two" value="Two" v-model="picked">
<label for="two">Two</label>
<br>
<span>Picked: {{ picked }}</span>
<!--选择列表-->
<select v-model="selected">
  <option>A</option>
  <option>B</option>
  <option>C</option>
</select>
<span>Selected: {{ selected }}</span>
<!--修饰符-->
<!-- 在 "change" 而不是 "input" 事件中更新 -->
<input v-model.lazy="msg" >
<!-- 将age 转为num -->
<input v-model.number="age" type="number">
<!-- 去除msg空格 -->
<input v-model.trim="msg">
```

 
### 总结

尝试了vue 各种简单事例，感觉还是可以简省不少现在的js代码。

- 动态的复制替换html内容
- 动态的生成html 

感觉vue 是比较强大的，需要进一步学习。


#### 参考：

* [http://cn.vuejs.org/v2/guide/](http://cn.vuejs.org/v2/guide/)