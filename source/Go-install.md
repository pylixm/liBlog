---
layout : post
title : 【 Go语言学习笔记 】 - Golang 环境搭建及相关概念
category : golang
date : 2018-01-25
tags : [golang, 语言学习]
---


## 环境搭建 

在环境搭建之前，先来了解几个常用的 Golang 环境变量：

- **$GOROOT** 表示 Go 在你的电脑上的安装位置，它的值一般都是 $HOME/go，当然，你也可以安装在别的地方。
- **$GOARCH** 表示目标机器的处理器架构，它的值可以是 386、amd64 或 arm。
- **$GOOS** 表示目标机器的操作系统，它的值可以是 darwin、freebsd、linux 或 windows。
- **$GOBIN** 表示编译器和链接器的安装位置，默认是 $GOROOT/bin，如果你使用的是 Go 1.0.3 及以后的版本，一般情况下你可以将它的值设置为空，Go 将会使用前面提到的默认值。
- **$GOPATH** 默认采用和 $GOROOT 一样的值，但从 Go 1.1 版本开始，你必须修改为其它路径。它可以包含多个包含 Go 语言源码文件、包文件和可执行文件的路径，而这些路径下又必须分别包含三个规定的目录：src、pkg 和 bin，这三个目录分别用于存放源码文件、包文件和可执行文件。
- **$GOARM** 专门针对基于 arm 架构的处理器，它的值可以是 5 或 6，默认为 6。
- **$GOMAXPROCS** 用于设置应用程序可使用的处理器个数与核数。
- **$GOHOSTOS** 交叉编译（运行机器和编译机器系统类型不同）时，设置本地机器系统类型，值会和本地机器（$GOOS 和 $GOARCH）一样。
- **$GOHOSTARCH** 交叉编译时，设置目标机器系统类型，值会和本地机器（$GOOS 和 $GOARCH）一样。
<!-- more -->
可运行 `go env` 查看更多环境变量。

```bash
$ go env
GOARCH="amd64"
GOBIN=""
GOEXE=""
GOHOSTARCH="amd64"
GOHOSTOS="darwin"
GOOS="darwin"
GOPATH="/Users/pylixm/go/"
GORACE=""
GOROOT="/usr/local/Cellar/go/1.9.2/libexec"
GOTOOLDIR="/usr/local/Cellar/go/1.9.2/libexec/pkg/tool/darwin_amd64"
GCCGO="gccgo"
CC="clang"
GOGCCFLAGS="-fPIC -m64 -pthread -fno-caret-diagnostics -Qunused-arguments -fmessage-length=0 -fdebug-prefix-map=/var/folders/hn/nsd6fjdd68z6kblbqvj6t1mm0000gn/T/go-build453502664=/tmp/go-build -gno-record-gcc-switches -fno-common"
CXX="clang++"
CGO_ENABLED="1"
CGO_CFLAGS="-g -O2"
CGO_CPPFLAGS=""
CGO_CXXFLAGS="-g -O2"
CGO_FFLAGS="-g -O2"
CGO_LDFLAGS="-g -O2"
PKG_CONFIG="pkg-config"
```

### 安装 

#### Linux, and FreeBSD tarballs

```bash
# 下载源码包
wget https://dl.google.com/go/go1.9.3.linux-amd64.tar.gz

# 解压到 /usr/local
tar -C /usr/local -xzf go$VERSION.$OS-$ARCH.tar.gz

# 配置环境变量  $HOME/.bash_profile
export PATH=$PATH:/usr/local/go/bin
source .bash_profile 
```

####  Mac OS X

Mac 系统可以使用同 Linux 相同方式的安装，也使用 brew 等包管理工具安装。

```bash
brew install go 
```

#### windows 

可直接在官方下载地址下载 msi 格式安装包安装。 官方下载地址： [https://golang.google.cn/dl/](https://golang.google.cn/dl/)

默认安装位置， c:\Go。

更多信息，可参考官方安装指导，[这里](https://golang.google.cn/doc/install)。

#### 测试安装 

在任意位置执行 `go version` 可看到go 的相关版本信息。

```bash
# go version
go version go1.9.3 linux/amd64
```

在任意目录，创建文件 hello.go 文件，内容如下：
```go
package main

import "fmt"

func main() {
    fmt.Printf("hello, world\n")
}
```
执行 `go run hello.go`，打印如下：
```
hello ,world
```

则说明安装成功。

#### 自定义安装位置

Linux 和 Mac 可在解压 Golang 时，将位置变换即可。golang 的安装包为开箱即用的。windows 也可在安装时修改。官方文档说，自定义了安装位置，必须配置 `GOROOT`。 

在Linux 测试，更换了安装位置，修改对应 go bin 的系统环境PATH 目录，执行go命令正常执行。通过`go env` 查看 GOROOT 自动修改为新的位置。

### 卸载 

直接删除 golang 目录（Linux/Mac OS: /usr/local/go; Windows: C:\Go ）和环境变量即可。

## 相关概念 

### 工作区和GOPATH 

工作区，是放置 Go 源码文件的目录。一般情况下，Go 源码文件都需要放到工作区中，但是对于命令源码文件来说，不是必须的。

工作区结构如下：
```bash
$ tree -d -L 1
.
├── bin
├── pkg
└── src
```

- **src** 用于放置源码文件，以代码包为组织形式。
- **pkg** 用于存放归档文件，以 .a 为后缀的文件，存放在相关平台目录下，同样以代码包为组织形式。 目录结构为： `$GOPATH/pkg/$GOOS_$GOARCH/<一级代码包>/<二级代码包>/<末级代码包>.a`
- **bin** 用于存放当前工作区的 Go 程序的可执行文件。
    - 当环境变量设置 GOBIN 时，该目录变得无意义，所有可执行文件（编译文件）会放到 GOBIN 的目录中；
    - 当 GOPATH 设置了多个目录时，必须设置 GOBIN 否则无法成功安装 Go 程序的可执行文件。

整体如下：
![](/static/imgs/gopath_demo.png)

### 源码文件类型

Go 源码文件以 .go 为后缀，所有源码文件都是以包为组织形式的。源码文件分3类：

- 命令源码文件：声明自己属于main代码包、包含无参数声明和结果声明的main函数。 go 程序的入口，不建议把所有文件都写在一个文件中。同一个代码包中不建议直接包含多个命令源码文件。安装后，存放在 GOBIN 或 <工作区>/bin 下 。
- 库源码文件：不具备命令源码文件两个特征的一般文件。被安装后，存放在 <工作区>/pkg/<相关平台目录> 下。
- 测试源码文件： 不具备命令源码文件两个特征的一般文件，以 _test.go 为后缀。其中至少有一个函数的命令以 Test 或 Benchmark 为前缀。


### 代码包的相关知识

**代码包的作用**
- 编译和归档 Go 程序的最基本单位。
- 代码划分、集结和依赖的有效组织形式，也是权限控制的辅助手段。

**代码包的规则**

一个代码包实际上就是一个有导入路径代表的目录。导入路径即 <工作区目录>/src 或 <工作区目录>/pkg/<平台相关目录> 之下的某段子路径。

**代码包的声明**

- 每个源码文件必须声明其所属的代码包。
- 同一个代码包中的所有源码文件声明的代码包应该是相同的。

**代码包声明与代码包导入路径的区别**

代码包声明语句中的包名称应该是该代码包的导入路径的最右子路径。如： 
代码包导入路径： `GoPL/tools/`
代码包声明：`package tools` 

**代码包的导入**

代码包导入语句中使用的包名称应该与其导入路径一至，如代码包 `fmt` 的导入：
```
import (
    "fmt"
)
```

**代码包的导入方法**

- 带别名的导入： 
```go
import str "strings" 

str.HasPrefix("abc","a")
```

- 本地化的导入：
```go
import . "strings" 

HasPrefix("abc","a")
```

- 仅仅初始化
```go
import _ "strings"

// 仅执行代码包中的初始化函数
```

**代码包初始化**

代码包初始化函数即：无参数声明和结果声明的 init 函数。init 函数可以被声明在任何文件中，且可以有多个。

init 函数执行时机：
- 单一代码包：当导入代码包时，对代码包的所有全局变量进行求值，之后执行所有 init 函数。同一代码包中，的 init 函数执行顺序是不确定的。
- 不同代码包：先执行被导入的代码包中的 init 函数，再执行本代码包的 init 函数。同一代码包中被导入多个代码包的 init 函数执行顺序不定。
- 所有涉及到的代码包：在程序入口，在 main 函数执行之前执行。所有的 init 函数，都只会被执行一次。

## 小结 

Golang 的安装可谓简单实用，开箱即用。对 Mac 和 Windows 系统都提供了对应的安装包，方便大家安装。

## 参考

- [https://golang.google.cn/doc/install](https://golang.google.cn/doc/install)
- [视频：Go语言第一课 郝林](https://www.imooc.com/learn/345)