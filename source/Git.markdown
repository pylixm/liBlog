---
layout : post
title : Git使用学习笔记
category : vcs
date : 2015-11-01
tags : [vcs]
---


## 一、Git知识点

1. 将发生变化的文件全部保存。为了减少磁盘使用，只保存发生变化的文件。使用sha1算法的20字节（40位）值作为对象的唯一标识。
![][1]

2. 三个域：
repository -- 仓库
working directory -- 工作区
staging area/index -- 过渡区
![][2]

3. 三个对象：
tree ：记录文件名，及指向blob的指针 
blob ：记录文件内容
commit ：和tree是一一对应的
find .git/objects/ -type f |wc -l
git cat-file -t sha1码
git show -s --pretty=raw xxx

4. 三个引用：
HEAD
branch
remote branch

5. 其他：
对象是静止的，引用是动态的。

<!-- more -->
## 二、操作使用

### git配置

1.文件位置

用户目录下的全局配置文件：
C:\Users\Administrator\.gitconfig
各仓库自己的配置文件：
D:\gitdemo\.git\config

2.用户配置：

```bash
# 全局，
git config --global user.name 'pyli.xm'
git config --global user.email 'pyli.xm@gmail.com'
# 局部，
git config  user.name 'pyli.xm'
git config  user.email 'pyli.xm@gmail.com'
```
### 命令

1、git初始化

```bash
    git init 
```
    
2、添加文件

    git add # 文件名

3、提交

```bash
git commit -m '说明'
# 添加并提交 
git commit -a -m '说明'
# 移除受控文件，
git rm -r -n --cached */Runtime/\* #预览剔除版本控制的文件  --cached 保留本地
git rm -r --cached */Runtime/\* #剔除版本控制 
git commit -am "移除Runtime目录下所有文件的版本控制"
git push
```

4、标签

```bash
# 创建：
git tag 标签名
# 打包：
git archive --format=tar --prefix=gitdemo/ 标签名|gzip > /gitdemo/gitdemo.tar.gz
# 检出：
git checkout 标签名
# 删除 
git tag -d tagname
# 提交tag到远程
git push [origin] --tags
# 删除远程tag
$ git push origin :refs/tags/tagname
```

5、分支 

```bash
#列出
git branch -l/-all
#创建：
git branch 分支名
#分支提交
git push origin 分支名
#分支切换 
git checkout  分支名
# 创建分之并切换分之
git checkout -b 分支名
#分支合并：
git merge 分支名A  在B分之下执行，将A合并到B分支上。
#删掉分支  
git branch -D 分支名A
#删除远程分支（>v1.7）
git push origin --delete <branchName>
# 修改分支名称
> git branch -m devel develop
```

6、回溯

单个文件：

```bash
git log -3
```

![][3]

```bash
# 使用此方法回溯单个文件的版本。
git check f0a843a92216d103cec18c746dd7a0b1ed5b0020  [文件路径] 
```

整个版本库：

```bash
本地库回滚：
git reset --hard <commit ID号> 或者 git reset --hard HEAD^
远程库回滚：
原理：先将本地分支退回到某个commit，删除远程分支，再重新push本地分支
操作步骤：
1、git checkout the_branch
2、git pull
3、git branch the_branch_backup //备份一下这个分支当前的情况
4、git reset --hard the_commit_id //把the_branch本地回滚到the_commit_id
5、git push origin :the_branch //删除远程 the_branch
6、git push origin the_branch //用回滚后的本地分支重新建立远程分支
7、git push origin :the_branch_backup //如果前面都成功了，删除这个备份分支
```


![][5]


7、查看当前修改了那些文件

![][4]

8、合并
```bash
# 分支合并：
git merge 分支名A  在B分之下执行，将B合并到A分支上。
# 在B分之下执行，将A合并到B分支上。
git merge --no-ff 分支A 
# 合并提交 
> git rebase -i HEAD~3
看到如下信息：
pick:*******
pick:*******
pick:*******
修改成：
pick:*******
squash:*******
squash:*******
保存退出，提示录入commit信息，保存即可。
```

9、其他
```
# 修改历史commit信息
> git rebase -i HEAD~3（3位从当前commit往前的个数）
看到如下信息：
pick:*******
pick:*******
pick:*******
如果你要修改哪个，就把那行的pick改成edit，然后退出。
> git commit --amend
> git rebase --continue

# 合并当前分支的commit
>git rebase -i HEAD~3 
看到如下信息：
pick:*******
pick:*******
pick:*******

- Commands:
- p, pick = git会应用这个补丁，以同样的提交信息（commit message）保存提交
- r, reword = ugit会应用这个补丁，但需要重新编辑提交信息
- e, edit = git会应用这个补丁，但会因为修订（amending）而终止
- s, squash = git会应用这个补丁，但会与之前的提交合并
- f, fixup = git会应用这个补丁，但会丢掉提交日志
- x, exec = git会在shell中运行这个命令
- d, drop = 直接删除该commit

从以上关键字说明，我们可以看出，与之前分支合并则使用 squash 关键字。
把rebase信息改为如下：
pick:*******
squash:*******
squash:*******

保存退出，会看到合并之后的所有commit的提交信息，大概如下：

# This is a combination of 2 commits.
# This is the 1st commit message:

init readme

# This is the commit message #2:

Create CONTRIBUTING.md

直接修改保存即可。注意此处的提交信心不能为空。



# 查看远端和本地分支情况
> git remote show origin

# 根据远端分支修建本地分支，将远端分支删除的分支在本地也删除
> git fetch -p / git remote prune origin 

# 查看文件提交情况
> git blame 文件名
显示格式：
commit ID | 代码提交作者 | 提交时间 | 代码位于文件中的行数 | 实际代码

# 查看每次提交的信息
> git show commitID

# 撤销 reset 
$ git reflog
b7057a9 HEAD@{0}: reset: moving to b7057a9
98abc5a HEAD@{1}: commit: more stuff added to foo
b7057a9 HEAD@{2}: commit (initial): initial commit

$ git reset --hard 98abc5a

```


**更多实例参考 ``git --help``** 

### 参考资料

[阮一峰-git分支管理策略](http://www.ruanyifeng.com/blog/2012/07/git.html)
[阮一峰-git工作流程](http://www.ruanyifeng.com/blog/2015/12/git-workflow.html)
[阮一峰-git常用命令清单](http://www.ruanyifeng.com/blog/2015/12/git-cheat-sheet.html)
[阮一峰-git远程操作详解](http://www.ruanyifeng.com/blog/2014/06/git_remote.html)


---

[1]:/static/imgs/git-1.png
[2]:/static/imgs/git-2.png
[3]:/static/imgs/git-3.png
[4]:/static/imgs/git-4.png
[5]:/static/imgs/git-5.png