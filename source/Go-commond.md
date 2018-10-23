---
layout : post
title : 【 Go语言学习笔记 】 - Golang 命令
category : golang
date : 2018-01-26
tags : [golang, 语言学习]
---

安装好 golang 后，在任意目录运行 `go` 可看到 Golang 的所有命令，如下：
```bash
	build       compile packages and dependencies
	clean       remove object files
	doc         show documentation for package or symbol
	env         print Go environment information
	bug         start a bug report
	fix         run go tool fix on packages
	fmt         run gofmt on package sources
	generate    generate Go files by processing source
	get         download and install packages and dependencies
	install     compile and install packages and dependencies
	list        list packages
	run         compile and run Go program
	test        test packages
	tool        run specified go tool
	version     print Go version
	vet         run go tool vet on packages
```

这里根据郝林老师的课程，做部分命令的总结，记录备查。
<!-- more -->
## 常用 Golang 命令总结 

### go run 

用于运行命令源文件，只接受一个命令源文件以及若干个库文件作为参数。内部操作步骤为，先编译，将编译结果放到临时文件（可执行文件和归档文件），再运行。

**运行常用标记：**
- `-a` 强制编译相关代码，不论他们的编译结果是否已经是最新的。
- `-n` 打印编译过程中所需要运行的命令，但不真正执行他们。
- `-x` 打印编译过程中运行的命令，并执行他们。
- `-p n` 并行执行，n 为并行的数量。
- `-v` 列出被编译的代码包的名称。
- `-work` 显示编译时创建的临时工作目录的路径，并且不删除它。

### go build 

用于编译我们指定的源码文件或代码包以及它们的依赖包。编译非命令源码文件是不会产生任何结果文件的。编译命令源码文件会在该命令的执行目录中生成一个可执行文件。

- 执行该命令且不追加任何参数，默认会把当前目录作为代码包编译
- 执行命令且以代码包导入路径为参数时，该代码包及其依赖代码包会被编译。当加入 -a 时，所有涉及到的代码包会被编译。
- 可加若干源码文件作为参数，go 只会编译被列出的源码文件  

**运行常用标记：同 go run**


### go install 

用于编译并安装代码包或源码文件。安装代码包会在当前工作区的 pkg/<平台相关目录> 下生成归档文件。安装命令源码文件会在当前工作区的 bin 目录 或 $GOBIN 目录下生成可执行文件。

- 不加参数时，它试图把当前目录作为代码包安装
- 加代码包导入路径作为参数，会安装该代码包及依赖包 

### go get 

用于从远程代码仓库上下载并按照代码包。支持版本控制系统， git/hg/svn/Bazaar等。指定的代码包会被下载到 $GOPATH 中包含的第一个工作区的 src 目录中。 

**运行常用标记：**
- `-d` 只下载，不安装。
- `-fix` 在下载代码包后，执行修正动作(go不同版本，语法的修正)
- `-u` 更新下已有的代码包及其依赖包。 

## 参考 

- [Golang 命令教程](https://github.com/hyper0x/go_command_tutorial/blob/master/SUMMARY.md)