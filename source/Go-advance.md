---
layout : post
title : 【 Go语言学习笔记 】 - Golang 语法进阶
category : golang
date : 2018-04-26
tags : [golang, 语言学习]
---

## 编码

- Go 原生支持UTF-8, 可直接打印非ASCII码字符。
```go
package main

import "fmt"

func main() {
    fmt.Printf("Hello, world or 你好，世界 or καλημ ́ρα κóσμ or こんにちはせかい\n")
}
```
- 可以使用任意UTF-8 字符作为标识符，但不建议。


## 导入

- Go 以包作为代码的最小组织单位，通过包来实现代码的导入、权限的控制。
- 每个go文件必须从以`package` 包声明开头，声明包名称最好和目录相同，也可以不同。不同时，注意`import` 引入时，为目录名，在引入后的调用使用中，使用该引入包的 `package` 声明名称。
- 三种导入方式：
```go
// 带别名的导入
import str "strings" 
str.HasPrefix("abc","a")

// 本地化的导入, 使用导入包中的函数时可不写模块名
import . "strings" 
HasPrefix("abc","a")

// 仅执行代码包中的初始化函数
import _ "strings"
```

- 一个package级别的func, type, 变量, 常量, 在package内部下无论大小,无需导入,可以随意访问。此时需要run整个包的编译文件：
```bash
awesomeProject
├── awesomeProject # go build 后产生
├── main.go
└── second.go
```
如下运行:
```
go run *.go 
./awesomeProject
```

## Go 基础

### 基本数据类型

- 字符串类型是不可变的，无法使用下标的方式访问。

### 声明

- 简要声明只能在函数中使用。
- 区分简要声明与赋值，防止简要声明造成的全局变量重新声明的问题。

## 函数

- Go 函数支持可变参数
```go
func myfunc(arg ...int) {}
```
- 参数为值类型：其实是传了一个参数的副本，函数中修改参数的值，并不会影响函数外参数的值。
- 参数为指针类型或引用类型：传入了一个指向数据值得一个指针副本，当改变该指针对应的值时，实际上是改变了函数外指针对应的值。
- 传指针比较轻量级 (8bytes),当传入函数的参数占用较大内存时，使用指针参数，会节省参数赋值的时间和内存开销，提升效率。常用于结构体作为参数传入函数时。
- Go语言中channel，slice，map这三种类型的实现机制类似指针，所以可以直接传递，而不用取地址后传递指针。（注：若函数需改变slice的长度，则仍需要取地址传递指针）
- 函数也可作为参数来传递
```go
package main
import "fmt"

type testInt func(int) bool // 声明了一个函数类型

func isOdd(integer int) bool {
    if integer%2 == 0 {
        return false
    }
    return true
}

func isEven(integer int) bool {
    if integer%2 == 0 {
        return true
    }
    return false
}

// 声明的函数类型在这个地方当做了一个参数

func filter(slice []int, f testInt) []int {
    var result []int
    for _, value := range slice {
        if f(value) {
            result = append(result, value)
        }
    }
    return result
}

func main(){
    slice := []int {1, 2, 3, 4, 5, 7}
    fmt.Println("slice = ", slice)
    odd := filter(slice, isOdd)    // 函数当做值来传递了
    fmt.Println("Odd elements of slice are: ", odd)
    even := filter(slice, isEven)  // 函数当做值来传递了
    fmt.Println("Even elements of slice are: ", even)
}
```

## Struct 结构体

- 结构体是类型的集合
- 结构体和通过`匿名结构体`来实现结构体字段的继承
```go
package main
import "fmt"

type Human struct {
    name string
    age int
    weight int
}

type Student struct {
    Human  // 匿名字段，那么默认Student就包含了Human的所有字段
    speciality string
}

func main() {
    // 我们初始化一个学生
    mark := Student{Human{"Mark", 25, 120}, "Computer Science"}

    // 我们访问相应的字段
    fmt.Println("His name is ", mark.name)
    fmt.Println("His age is ", mark.age)
    fmt.Println("His weight is ", mark.weight)
    fmt.Println("His speciality is ", mark.speciality)
    // 修改对应的备注信息
    mark.speciality = "AI"
    fmt.Println("Mark changed his speciality")
    fmt.Println("His speciality is ", mark.speciality)
    // 修改他的年龄信息
    fmt.Println("Mark become old")
    mark.age = 46
    fmt.Println("His age is", mark.age)
    // 修改他的体重信息
    fmt.Println("Mark is not an athlet anymore")
    mark.weight += 60
    fmt.Println("His weight is", mark.weight)
}
```
![](static/imgs/student_struct.png)

## 方法

- 方法多了一个接受者（所属者）的func:  `func (r ReceiverType) funcName(parameters) (results)`
- receiver 可以是任何你自定义的类型、内置类型等各种类型。
- 当指针作为receiver时，引用其方法可以直接使用指针对应的对象。
- 方法可以通过匿名结构体来继承。
- 方法的调用顺序是，先调用当前结构体的方法，再调用其继承的方法。所以，可以通过重新本结构体的方法，来达到方法重写的目的。
```go
package main
import "fmt"

type Human struct {
    name string
    age int
    phone string
}

type Student struct {
    Human //匿名字段
    school string
}

type Employee struct {
    Human //匿名字段
    company string
}

//Human定义method
func (h *Human) SayHi() {
    fmt.Printf("Hi, I am %s you can call me on %s\n", h.name, h.phone)
}

//Employee的method重写Human的method
func (e *Employee) SayHi() {
    fmt.Printf("Hi, I am %s, I work at %s. Call me on %s\n", e.name,
        e.company, e.phone) //Yes you can split into 2 lines here.
}

func main() {
    mark := Student{Human{"Mark", 25, "222-222-YYYY"}, "MIT"}
    sam := Employee{Human{"Sam", 45, "111-888-XXXX"}, "Golang Inc"}

    mark.SayHi()
    sam.SayHi()
}
```

## 接口

- 接口为一组抽象方法的集合，它必须由其他非interface类型实现，而不能自我实现。
- 空接口 `interface(interface{})`, 可认为任何类型都实现了空接口。
- 接口变量可以存储任何实现了接口的类型，空接口变量可以存储任何类型数据。
- 当接口作为函数参数时，则该参数可以为任何实现了该接口的数据类型。
```go
package main

import (
    "fmt"
    "strconv"
)

type Element interface{}
type List [] Element

type Person struct {
    name string
    age int
}

//定义了String方法，实现了fmt.Stringer接口
func (p Person) String() string {
    return "(name: " + p.name + " - age: "+strconv.Itoa(p.age)+ " years)"
}

func main() {
    list := make(List, 3)
    list[0] = 1 // an int
    list[1] = "Hello" // a string
    list[2] = Person{"Dennis", 70}

    for index, element := range list {
        // value, ok = element.(T) 判断是是否是T类型
        if value, ok := element.(int); ok {
            fmt.Printf("list[%d] is an int and its value is %d\n", index, value)
        } else if value, ok := element.(string); ok {
            fmt.Printf("list[%d] is a string and its value is %s\n", index, value)
        } else if value, ok := element.(Person); ok {
            fmt.Printf("list[%d] is a Person and its value is %s\n", index, value)
        } else {
            fmt.Printf("list[%d] is of a different type\n", index)
        }
    }
}
```

- 接口可通过嵌套接口来继承接口的方法。
- Go 语言支持反射
```go
t := reflect.TypeOf(i)    //得到类型的元数据,通过t我们能获取类型定义里面的所有元素
v := reflect.ValueOf(i)   //得到实际的值，通过v我们获取存储在里面的值，还可以去改变值
```

## 并发

- 线程同步：
```go
// 使用 sync.Mutex
func main() {
    var mu sync.Mutex

    mu.Lock()
    go func(){
        fmt.Println("你好, 世界")
        mu.Unlock()
    }()

    mu.Lock()
}
// 使用无缓存channal
func main() {
    done := make(chan int)

    go func(){
        fmt.Println("你好, 世界")
        <-done
    }()

    done <- 1
}
// 使用有缓存channal
func main() {
    done := make(chan int, 10) // 带 10 个缓存

    // 开N个后台打印线程
    for i := 0; i < cap(done); i++ {
        go func(){
            fmt.Println("你好, 世界")
            done <- 1
        }()
    }

    // 等待N个后台线程完成
    for i := 0; i < cap(done); i++ {
        <-done
    }
}
// 对于阻塞N个线程完成后再继续执行，可使用 WaitGroup 
func main() {
    var wg sync.WaitGroup

    // 开N个后台打印线程
    for i := 0; i < 10; i++ {
        wg.Add(1)

        go func() {
            fmt.Println("你好, 世界")
             wg.Done()
         }()
    }

    // 等待N个后台线程完成
    wg.Wait()
}
```

- 开启多个并发，只要有1个返回，既退出住线程。
```go
func main() {
    ch := make(chan string, 32)

    go func() {
        ch <- searchByBing("golang")
    }
    go func() {
        ch <- searchByGoogle("golang")
    }
    go func() {
        ch <- searchByBaidu("golang")
    }

    fmt.Println(<-ch)
}
```

- 生产者消费者模型
```go
// Package pubsub implements a simple multi-topic pub-sub library.
package pubsub

import (
    "sync"
    "time"
)

type (
    subscriber chan interface{}         // 订阅者为一个管道
    topicFunc  func(v interface{}) bool // 主题为一个过滤器
)

// 发布者对象
type Publisher struct {
    m           sync.RWMutex             // 读写锁
    buffer      int                      // 订阅队列的缓存大小
    timeout     time.Duration            // 发布超时时间
    subscribers map[subscriber]topicFunc // 订阅者信息
}

// 构建一个发布者对象, 可以设置发布超时时间和缓存队列的长度
func NewPublisher(publishTimeout time.Duration, buffer int) *Publisher {
    return &Publisher{
        buffer:      buffer,
        timeout:     publishTimeout,
        subscribers: make(map[subscriber]topicFunc),
    }
}

// 添加一个新的订阅者，订阅全部主题
func (p *Publisher) Subscribe() chan interface{} {
    return p.SubscribeTopic(nil)
}

// 添加一个新的订阅者，订阅过滤器筛选后的主题
func (p *Publisher) SubscribeTopic(topic topicFunc) chan interface{} {
    ch := make(chan interface{}, p.buffer)
    p.m.Lock()
    p.subscribers[ch] = topic
    p.m.Unlock()
    return ch
}

// 退出订阅
func (p *Publisher) Evict(sub chan interface{}) {
    p.m.Lock()
    defer p.m.Unlock()

    delete(p.subscribers, sub)
    close(sub)
}

// 发布一个主题
func (p *Publisher) Publish(v interface{}) {
    p.m.RLock()
    defer p.m.RUnlock()

    var wg sync.WaitGroup
    for sub, topic := range p.subscribers {
        wg.Add(1)
        go p.sendTopic(sub, topic, v, &wg)
    }
    wg.Wait()
}

// 关闭发布者对象，同时关闭所有的订阅者管道。
func (p *Publisher) Close() {
    p.m.Lock()
    defer p.m.Unlock()

    for sub := range p.subscribers {
        delete(p.subscribers, sub)
        close(sub)
    }
}

// 发送主题，可以容忍一定的超时
func (p *Publisher) sendTopic(sub subscriber, topic topicFunc, v interface{}, wg *sync.WaitGroup) {
    defer wg.Done()
    if topic != nil && !topic(v) {
        return
    }

    select {
    case sub <- v:
    case <-time.After(p.timeout):
    }
}

// main.go 
import "path/to/pubsub"

func main() {
    p := pubsub.NewPublisher(100*time.Millisecond, 10)
    defer p.Close()

    all := p.Subscribe()
    golang := p.SubscribeTopic(func(v interface{}) bool {
        if s, ok := v.(string); ok {
            return strings.Contains(s, "golang")
        }
        return false
    })

    p.Publish("hello,  world!")
    p.Publish("hello, golang!")

    go func() {
        for  msg := range all {
            fmt.Println("all:", msg)
        }
    } ()

    go func() {
        for  msg := range golang {
            fmt.Println("golang:", msg)
        }
    } ()

    // 运行一定时间后退出
    time.Sleep(3 * time.Second)
}
```



## 参考

- [https://chai2010.gitbooks.io/advanced-go-programming-book/content/ch1-basic/ch1-06-goroutine.html](https://chai2010.gitbooks.io/advanced-go-programming-book/content/ch1-basic/ch1-06-goroutine.html)
- [https://www.kancloud.cn/kancloud/web-application-with-golang/44111](https://www.kancloud.cn/kancloud/web-application-with-golang/44111)