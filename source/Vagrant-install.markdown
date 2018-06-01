---
layout : post
title : vagrant的开发环境搭建-windows开发环境为例
category : 虚拟机
date : 2015-12-01 11:30:00
tags : [容器, 虚拟机]
---



前几天看了vagrant的介绍，今天正好有空，打算安装下试试。由于自己用的是windows的开发环境，所以就在window下试着搭建了下。遇到一些问题，记录下。

关于vagrant，及为什么用vagrant。大家可以去看这篇文章《[为什么要使用Vagrant](http://www.ituring.com.cn/article/131600)》,个人感觉说的比较详细。

接下来，说下我的整个安装过程。

### 一、准备工作
---

* 开源虚拟软件 virtualbox ：https://www.virtualbox.org/

* Vagrant 安装包 ：http://www.vagrantup.com/

* box 的镜像文件 

vagrant 除了virtualbox，还支持HyperV、VMWare等虚拟软件。virtualbox与vagrant是最常用的搭配，也是文档最多的，所以我也选了这对组合。

box 的镜像除了使用下载好的本地文件还可以使用在线的box镜像，添加镜像时，还是会下载。

### 二、安装及应用
---

**2.1 安装virtualbox和vagrant**

同其他windows软件一样，“下一步”即可。

**2.2 应用**

1、给vagrant 添加镜像。

```bash
D:\vagrant\>vagrant box add base centos-6.6-x86_64.box
```

说明：

* ``vagrant box`` vagrant命令
* ``base`` 添加box的名称
* ``centos-6.6-x86_64.box-`` 本地box的文件名
* 使用``vagrant box list `` 查看添加的box镜像列表。

也可以添加在线box，和添加本地box一样。通过命令``vagrant box add ubuntu/trusty64``。ubuntu/trusty64为在线镜像名称。

在线镜像地址 [vagrantCloud](https://vagrantcloud.com/boxes/search)。（国内的网络访问可能不太通，建议下载后添加 ）

这是我使用centos的镜像 [centos-6.6-x86_64.box](http://pan.baidu.com/s/1hqsFS48)

2、初始化虚拟机。

```bash
D:\\vagrant\\>mkdir worker # 创建工作环境
D:\\vagrant\\>cd worker 
D:\\vagarnt\\worker\\>vagrant init [boxname] # 当添加的box的别名不为 base 时，此处需要添加 boxname
```

3、启动虚拟机

```bash
D:\\vagrant\\worker\\>vagrant up 
```

看到如下信息，说明虚拟机启动成功：
    
    D:\vagrant\worker>vagrant up
    Bringing machine 'default' up with 'virtualbox' provider...
    ==> default: Importing base box 'base'...
    ==> default: Matching MAC address for NAT networking...
    ==> default: Setting the name of the VM: worker_default_1448939529781_46842
    ==> default: Clearing any previously set forwarded ports...
    ==> default: Clearing any previously set network interfaces...
    ==> default: Preparing network interfaces based on configuration...
        default: Adapter 1: nat
        default: Adapter 2: hostonly
    ==> default: Forwarding ports...
        default: 22 => 2222 (adapter 1)
    ==> default: Booting VM...
    ==> default: Waiting for machine to boot. This may take a few minutes...
        default: SSH address: 127.0.0.1:2222
        default: SSH username: vagrant
        default: SSH auth method: private key
        default: Warning: Connection timeout. Retrying...
        default: Warning: Connection timeout. Retrying...
        default: Warning: Remote connection disconnect. Retrying...
        default:
        default: Vagrant insecure key detected. Vagrant will automatically replace
        default: this with a newly generated keypair for better security.
        default:
        default: Inserting generated public key within guest...
        default: Removing insecure key from the guest if it's present...
        default: Key inserted! Disconnecting and reconnecting using new SSH key...
    ==> default: Machine booted and ready!
    ==> default: Checking for guest additions in VM...
        default: The guest additions on this VM do not match the installed version of
        default: VirtualBox! In most cases this is fine, but in rare cases it can
        default: prevent things such as shared folders from working properly. If you see
        default: shared folder errors, please make sure the guest additions within the
        default: virtual machine match the version of VirtualBox you have installed on
        default: your host and reload your VM.
        default:
        default: Guest Additions Version: 4.3.28
        default: VirtualBox Version: 5.0
    ==> default: Configuring and enabling network interfaces...
    ==> default: Mounting shared folders...
        default: /vagrant => D:/vagrant/worker

<font style="color:red;">注意：</font>
此处会有个错误，卡在此处：

    Bringing machine 'default' up with 'hyperv' provider...
    ==> default: Verifying Hyper-V is enabled...

经查找，网上许多网友说是vagrant的启动虚拟机时，使用了windows 系统自带的 hyperv 虚拟机导致。但他们的问题大部分是发生在windows 8上，而我的系统为window7 。

最后，看到有网友说需要配置虚拟机 virtualbox 的环境变量（将virtualbox的安装目录添加到环境变量path中），试了下果然解决我的问题。

20151217更新：

网络的配置，网络的配置在worker文件夹下的Vagrantfile 文件中。vagrant创建的虚拟机有3中配置网络模式：

- 较为常用是端口映射，就是将虚拟机中的端口映射到宿主机对应的端口直接使用 ，在Vagrantfile中配置：

    config.vm.network "forwarded_port", guest: 80, host: 8080

将配置直接去掉注释“#”即可。guest: 80 表示虚拟机中的80端口， host: 8080 表示映射到宿主机的8080端口。

- 如果需要自己自由的访问虚拟机，但是别人不需要访问虚拟机，可以使用private_network，并为虚拟机设置IP ，在Vagrantfile中配置：

    config.vm.network "private_network", ip: "192.168.56.2"

192.168.56.2 表示虚拟机的IP，多台虚拟机的话需要互相访问的话，设置在相同网段即可。该ip默认帮到eth1上。

- 如果需要将虚拟机作为当前局域网中的一台计算机，由局域网进行DHCP，那么在Vagrantfile中配置：

    config.vm.network :public_network

此时虚拟机就如同宿主机一样链接到网络中，享有和宿主机一样的网络权限。此时，若ip为自由分配，可使用127.0.0.1地址，

端口使用启动时在命令窗口提示的端口，登陆机器查看分配的ip，即可使用分配的ip登陆。若ip为固定的，可在配置中写好。如下：

    config.vm.network :"public_network"，ip: "192.168.56.2"
    #还可设置网桥，以无线为例 -- 此配置需验证，一般只需配置最简即可。
    config.vm.network "public_network", :bridge => 'en1: Wi-Fi (AirPort)'
    




4、链接使用

由于windows不支持 ssh 命令，所以我们需要使用其他的ssh的客户端来链接。就拿我使用的xshell来做说。

在cmd窗口中录入：``vagrant ssh``。会看到你的主机地址、端口、以及key的存放位置。

    D:\vagrant\worker>vagrant ssh
    `ssh` executable not found in any directories in the %PATH% variable. Is an
    SSH client installed? Try installing Cygwin, MinGW or Git, all of which
    contain an SSH client. Or use your favorite SSH client with the following
    authentication information shown below:
    
    Host: 127.0.0.1
    Port: 2222
    Username: vagrant
    Private key: D:/vagrant/worker/.vagrant/machines/default/virtualbox/private_key

在xshell中添加ssh的key。可以参考 [这里](http://www.aiezu.com/system/linux/xshell_ssh_public-key_login.html)。

由于我们的key已经生成，所以我们只需导入即可。

工具-->用户秘钥管理-->导入，即可。

![](/static/imgs/xshell-ssh.png)

创建好回话后，在点击登录的时候选择 public key ，会看到我们导入的 private_key。

![](/static/imgs/xshell-ssh2.png)

此处密码不用填写，直接点击登录即可进入系统命令行了。

到这里，便和操作普通的linux的系统一样了。

若想使用root用户登录，见下文 3.3 节。

5、打包分发

当你配置好开发环境后，退出并关闭虚拟机。在终端里对开发环境进行打包：

    vagrant package

打包完成后会在当前目录生成一个 package.box 的文件，将这个文件传给其他用户，其他用户只要添加这个 box 

并用其初始化自己的开发目录就能得到一个一模一样的开发环境了。


### 三、其他
---

#### 3.1 **常用命令**

虚拟机关机：``D:\\vagrant\\worker\\>vagrant halt``

虚拟机挂起：``D:\\vagrant\\worker\\>vagrant suspend``

虚拟机恢复：``D:\\vagrant\\worker\\>vagrant resume``

删除虚拟机：``D:\\vagrant\\worker\\>vagrant destory``

查看虚拟机运行状态: ``D:\\vagrant\\worker\\>vagrant status ``

重启虚拟机: ``D:\\vagrant\\worker\\>vagrant reload ``
 
 
#### 3.2 **Vagrant和VirtualBox配置修改**

Vagrant和VirtualBox安装完成后，默认存放虚拟机镜像文件的位置在系统盘。这对于大多数系统盘容量有限的人来说，

很快就会收到“磁盘容量不足”的告警。通过必要的设置将镜像数据移出系统盘。

**3.2.1 更改VirtualBox的镜像文件存放位置**

具体步骤如下：

1、打开VirtualBox，从菜单项选择 全局设置 （快捷键是 Ctrl-G ）

2、选择 常规 里的 默认虚拟电脑位置(M)

3、设置为非系统盘的位置。

4、将原位置中的虚拟机镜像移动到新的位置。

如果在设置前已经安装了虚拟机，那么在Windows 资源管理器中，选择对应目录中的 Vbox 文件，即可将新目录中的虚拟机镜像添加到VirtualBox中。

**3.2.2 更改Vagrant的镜像存储位置**

Vagrant对于虚拟机的管理分成两个部分：Box和Machine。Box是指初始的未部署的虚拟机镜像文件。这个文件相当于是虚拟机的一个模板，

可以进行无限制次数的复制。Machine，是指处于可运行状态下的虚拟机。当在Vagrant中添加box是，默认Vagrant会将这些虚拟机模板镜像文件存

放在c:\User\<Username>\.Vagrant.d里。

因此，当使用Vagrant管理的虚拟机模板镜像较多时，这个目录也是比较大的。可以转移到其他磁盘分区上。方法是：

1、将 c:\User\<username>\.vagrant.d 目录移动到新的位置

2、设置 VAGRANT_HOME 环境变量指向新的位置即可。
 

#### 3.3 **使用root用户登录虚拟机**

在linux系统下没有root权限是很不舒服的，所以查了下root用户登录的配置，在vagrantfile 中增加配置：

    config.ssh.username = 'root'
    config.ssh.password = 'vagrant'
    config.ssh.insert_key = 'true'

启动后看到日志 ：

    D:\vagrant\worker>vagrant up
    Bringing machine 'default' up with 'virtualbox' provider...
    ==> default: Clearing any previously set forwarded ports...
    ==> default: Clearing any previously set network interfaces...
    ==> default: Preparing network interfaces based on configuration...
        default: Adapter 1: nat
        default: Adapter 2: hostonly
    ==> default: Forwarding ports...
        default: 22 => 2222 (adapter 1)
    ==> default: Booting VM...
    ==> default: Waiting for machine to boot. This may take a few minutes...
        default: SSH address: 127.0.0.1:2222
        default: SSH username: root
        default: SSH auth method: password
        default: Warning: Connection timeout. Retrying...
        default: Warning: Connection timeout. Retrying...
    ==> default: Machine booted and ready!
    ==> default: Checking for guest additions in VM...
        default: The guest additions on this VM do not match the installed version of
        default: VirtualBox! In most cases this is fine, but in rare cases it can
        default: prevent things such as shared folders from working properly. If you see
        default: shared folder errors, please make sure the guest additions within the
        default: virtual machine match the version of VirtualBox you have installed on
        default: your host and reload your VM.
        default:
        default: Guest Additions Version: 4.3.28
        default: VirtualBox Version: 5.0
    ==> default: Configuring and enabling network interfaces...
    ==> default: Mounting shared folders...
        default: /vagrant => D:/vagrant/dev
    ==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
    ==> default: flag to force provisioning. Provisioners marked to run always will still run.

-- 2018-04-24 update 
注：此处注意错误`default: Warning: Authentication failure. Retrying...`
有些box镜像关闭了密码登录，可先不配置用户名密码使用`vagrant ssh`登录，修改`/etc/ssh/sshd_config`中的`PasswordAuthentication` 设置为 `yes`即可

#### 3.4 一个vagrantfile 文件管理多台虚机

1、先使用 box 初始化： `vagrant init `

2、修改配置文件如下：

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: "echo Hello"
  
  config.vm.define "master" do |saltmaster|
    saltmaster.vm.box = "base"
    saltmaster.vm.host_name = 'saltmaster.local'
    saltmaster.vm.network "private_network", ip: "192.168.33.13"
    saltmaster.ssh.username = 'root'
    saltmaster.ssh.password = 'vagrant'
    saltmaster.ssh.insert_key = 'true'
  end

  config.vm.define "minion" do |saltminion|
    saltminion.vm.box = "base"
    saltminion.vm.host_name = 'saltminion.local'
    saltminion.vm.network "private_network", ip: "192.168.33.14"
    saltminion.ssh.username = 'root'
    saltminion.ssh.password = 'vagrant'
    saltminion.ssh.insert_key = 'true'
  end
end
```

3、正常启动即可 : `vagrant up`

4、登录

- 使用 vagrant ssh + 名称 登录 
```bash
pylixm@pylixm-pc /d/vagrant/dev331314 $ vagrant ssh master
root@127.0.0.1's password:
Welcome to your Vagrant-built virtual machine.
[root@saltmaster ~]#
```

- 使用 ip 直接登录
 
#### 将已有 virtualbox 虚机添加到 vagrant管理

直接添加是不行的，这里提供了一中变向的方式：先将virtualbox 的虚机转成 box 镜像 ，再将镜像添加到 vagrant 管理；

详细 --> [这里](http://stackoverflow.com/questions/20560152/what-is-the-vagrant-syntax-for-adding-a-locally-existing-vdi)

1、打包已有虚机（虚机必须用virtualbox打开过，为了让virtualbox可以找到该虚机）

    vagrant package --base mybox --output /path/to/mybox.box

2、添加 box 镜像 

    vagrant box add mybox /path/to/mybox.box




## 错误问题汇总

#### Vagrant with VirtualBox on Windows10: “Rsync” could not be found on your PATH

http://stackoverflow.com/questions/34176041/vagrant-with-virtualbox-on-windows10-rsync-could-not-be-found-on-your-path

#### Failed to mount folders in Linux guest. 

https://github.com/mitchellh/vagrant/issues/3341

--- 

### 参考：

* [http://www.ituring.com.cn/article/131438](http://www.ituring.com.cn/article/131438)

* [http://ninghao.net/blog/2077](http://ninghao.net/blog/2077)

* [http://www.imooc.com/wenda/detail/243450](http://www.imooc.com/wenda/detail/243450)

* [http://blog.smdcn.net/article/1308.html](http://blog.smdcn.net/article/1308.html)

* [http://stackoverflow.com/questions/25758737/vagrant-login-as-root-by-default](http://stackoverflow.com/questions/25758737/vagrant-login-as-root-by-default)