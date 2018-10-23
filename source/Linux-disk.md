---
layout : post
title : Linux基础系列 - 磁盘相关操作命令总结
category : linux
date : 2018-09-30
tags : [linux, linux基础系列, 运维知识库]
---

Linux 系统中磁盘信息的查看是比较常用的操作，例如，查看磁盘使用情况、查看磁盘分区等待操作。这里总结一些运维中常用到的命令，以备使用查询。

## 磁盘的接口

现在磁盘最常用的可简单分为普通的机械盘和SSD(Solid-state drive或Solid-state disk)两种，他们都已不同的接口协议和主板链接，在了解命令之前，我们先来看下，现在服务器磁盘的接口协议。这样可以更好的了解磁盘。

<!-- more -->

现阶段磁盘的接口主要有以下几种：

**ATA**，全称Advanced Technology Attachment，是用传统的40-pin并口数据线连接主板与硬盘的，接口速度最大为133MB/s，因为并口线的抗干扰性太差，且排线占用空间较大，不利计算机内部散热，已逐渐被SATA所取代。

**SATA**，全称Serial ATA，也就是使用串口的ATA接口，因抗干扰性强，且对数据线的长度要求比ATA低很多，支持热插拔等功能，SATA-II的接口速度为300MiB/s，而新的SATA-III标准可达到600MiB/s的传输速度。SATA的数据线也比ATA的细得多，有利于机箱内的空气流通，整理线材也比较方便。

**SCSI**，全称是Small Computer System Interface（小型机系统接口），经历多代的发展，从早期的SCSI-II，到目前的Ultra320 SCSI以及Fiber-Channel（光纤通道），接口型式也多种多样。SCSI硬盘广为工作站级个人计算机以及服务器所使用，因此会使用较为先进的技术，如碟片转速15000rpm的高转速，且资料传输时CPU占用率较低，但是单价也比相同容量的ATA及SATA硬盘更加昂贵。

**SAS**（Serial Attached SCSI）是新一代的SCSI技术，和SATA硬盘相同，都是采取序列式技术以获得更高的传输速度，可达到6Gb/s。此外也透过缩小连接线改善系统内部空间等。

此外，由于SAS硬盘可以与SATA硬盘共享同样的背板，因此在同一个SAS存储系统中，可以用SATA硬盘来取代部分昂贵的SAS硬盘，节省整体的存储成本。但SATA存储系统并不能连接SAS硬盘。

**FC**（Fibre Channel，光纤通道接口），拥有此接口的硬盘在使用光纤联接时具有热插拔性、高速带宽（4Gb/s或10Gb/s）、远程连接等特点；内部传输速率也比普通硬盘更高。限制于其高昂的售价，通常用于高端服务器领域。


现在，普通机械盘接口多为SATA，固态盘接口多为SAS。更多磁盘知识可参考[Wiki百科](https://zh.wikipedia.org/wiki/%E7%A1%AC%E7%9B%98)。

## 磁盘信息查看相关命令

### lsscsi

该命令只支持 SCSI接口的磁盘。

```
-s 显示容量大小。
-c 用全称显示默认的信息。
-d 显示设备主，次设备号。
-g 显示对应的sg设备名。
-H 显示主机控制器列表，-Hl,-Hlv。
-l 显示相关属性，-ll,-lll=-L。
-v 显示设备属性所在目录。
-x 以16进制显示lun号。
-p 输出DIF,DIX 保护类型。
-P 输出有效的保护模式信息。
-i 显示udev相关的属性
-w 显示WWN
```

**实例**

```bash
[root@localhost]# lsscsi
[0:0:0:0]    disk    ATA      ST500DM002-1BD14 KC47  /dev/sda 
[5:0:0:0]    cd/dvd  HL-DT-ST DVD+-RW GHB0N    A100  /dev/sr0
```

### smartctl 

`smartctl`是磁盘工具包`smartmontools`中的命令。该工具包有自我监控(Self-Monitoring)、分析(Analysis)和报告(Reporting)三个模块组成，所以缩写为S.M.A.R.T或SMART。可使用系统包管理工具`yum`安装，我们这里只说`smartctl`这个命令的使用，其他更多使用大家可参考[官方文档](https://www.smartmontools.org/wiki/TocDoc)。

`smartctl`常用语法如下：

```
语法：

    smartctl  [options]  device

device：

	"/dev/hd[a-t]"    IDE/ATA 磁盘
	"/dev/sd[a-z]"    SCSI devices磁盘。注意，对于SATA磁盘，由于是通过libata

显示信息 参数参数：
-h  帮助信息
-V  版本信息
-i  打印基本信息（磁盘设备号、序列号、固件版本…）
-a  打印磁盘所有的SMART信息
-x  打印所有设备信息
-g Name 获取磁盘执行信息：
    name 取值 all, aam, apm, lookahead, security, wcache, rcache, wcreorder

运行时行为 参数：
-q  TYPE     指定输出的安静模式。
TYPE可以有3种选择：
      eorsonly    只打印错误日志。
      slent       有任何打印。
      nserial     不打印序列号

-d  TYPE     指定磁盘的类型。如果没有指定，smartctl会根据磁盘的名字来猜测磁盘类型。
             磁盘类型包括： ata, scsi, sat[,auto][,N][+TYPE], usbcypress[,X], usbjmicron[,p][,x][,N], usbsunplus, marvell, areca,N/E, 3ware,N, hpt,L/M/N, megaraid,N, cciss,N, auto, test

-T  TYPE     指定当发生错误时，smartctl的容忍程度，是否继续运行。
	 TYPE可以有4种选择：
	 conservative      一有错就会退出
	 normal        如果必须支持的SMART命令失败，则退出
	 permissive     忽略一次必须支持的SMART命令失败
	 verypermissive  忽略所有必须支持的SMART命令失败

-b  TYPE     指定当发生校验错误时，smartctl的动作。
     TYPE有3种选择：
       warn          发出警告，继续执行
       exit           退出smartctl
       ignore        不发出告警，继续执行      

-r  TYPE      smartmontools开发人员相关。

-n  POWERMODE    指定当磁盘处于节能模式时，smartctl是否继续检查，默认是不检查。

	POWERMODE有4种选择：
	  never   检查
	  sleep    除了sleep模式，检查。
	  standby  除了sleep或standby模式，检查。
	  idle      除了sleep或standby或idle模式，见车。

SMART功能开关 参数：
-s  on/off      打开或关闭磁盘的SMART功能
-o  on/off      打开或关闭SMART自动离线检测，该功能每4小时就会自动扫描磁盘是否有缺陷。
-S  on/off   打开或关闭“自动保存厂商指定属性”功能。

SMART 读和显示数据 参数
-H  报告磁盘的是否健康。如果报告不健康，则说明磁盘已经损坏或会在24小时内损坏。
-c  显示磁盘支持的普通SMART功能，以及这些功能当前的状态。
-A  显示磁盘支持的厂商指定SMART特性。这些特性的编号从1-253，并且有指定的名字。
-f  设置输出格式：old, brief, hex[,id|val]
-l  TYPE      指定显示的log类型。
     TYPE有4种选择：
     error             只显示error  log。
     selftest    只显示selftest  log
     selective 只显示selective  self-test  log
     directory 只显示Log  Directory

-v  N,OPTION    显示厂商指定SMART特性N时，使用厂商相关的显示方式。
-F  TYPE     设置smartctl的行为，当出现一些已知但还没有解决的硬件或软件bug时，smartctl应该怎么做。
-P  TYPE     设置smartctl是否对磁盘使用数据库中已有的参数。

SMART 离线测试、自测试 参数
-t  TEST      立刻执行测试，可以和-C参数一起使用。
     TEST可以有以下几个选择：
     offline  离线测试。可以在挂载文件系统的磁盘上使用
     short   短时间测试。可以在挂载文件系统的磁盘上使用。
     long   长时间测试。可以在挂载文件系统的磁盘上使用。
     conveyance  [ATA only]传输zi测试。可以在挂载文件系统的磁盘上使用。
     select, N-M    
	 select, N+SIZE  [ATA only]有选择性测试，测试磁盘的部分LBA。N表示LBA编号，M表示结束LBA编号，SIZE表示测试的LBA范围。


-C  在captive模式下运行测试。
注意：（1）-C必须配合-t一起使用，但如果是-t offline，则-C不生效。
     （2）-C会使得磁盘很忙，所以最好是在没有挂载文件系统的磁盘上使用。


-X  中断no-captive模式下运行的测试。
```

**实例**


```
smartctl --all /dev/hda     # 打印所有hda设备信息
smartctl --smart=on --offlineauto=on --saveauto=on /dev/hda   # 开启hda SMART 支持
smartctl --test=long /dev/hda   # 执行扩展磁盘自检

smartctl --attributes --log=selftest --quietmode=errorsonly /dev/hda  # 打印自检和属性错误

# 在3ware RAID控制器上打印第3个ATA磁盘的所有SMART信息
smartctl --all --device=3ware,2 /dev/sda
smartctl --all --device=3ware,2 /dev/twe0
smartctl --all --device=3ware,2 /dev/twa0
smartctl --all --device=3ware,2 /dev/twl0

# 打印连接到第3个PMPort的SATA磁盘的所有SMART信息第一个HighPoint RAID控制器上的第一个通道
smartctl --all --device=hpt,1/1/3 /dev/sda

# 打印Areca RAID控制器上第一个机箱的第3个ATA磁盘的所有SMART信息
smartctl --all --device=areca,3/1 /dev/sg2

# 打印raid 中，第4块盘的基本信息
smartctl -a -d megaraid,3 /dev/sda  
```

### MegaCli 

MegaCli是一款管理维护硬件RAID软件，可以通过它来了解当前raid卡的所有信息，包括 raid卡的型号，raid的阵列类型，raid 上各磁盘状态，等等。该工具可从以下链接下载：

```
http://www.lsi.com/downloads/Public/RAID%20Controllers/RAID%20Controllers%20Common%20Files/8.07.10_MegaCLI_Linux.zip
```

**常用命令**

```
#/opt/MegaRAID/MegaCli/MegaCli64 -LDInfo -Lall -aALL 查raid级别
#/opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aALL 查raid卡信息
#/opt/MegaRAID/MegaCli/MegaCli64 -PDList -aALL 查看硬盘信息
#/opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -aAll 查看电池信息
#/opt/MegaRAID/MegaCli/MegaCli64 -FwTermLog -Dsply -aALL 查看raid卡日志
#/opt/MegaRAID/MegaCli/MegaCli64 -adpCount 【显示适配器个数】
#/opt/MegaRAID/MegaCli/MegaCli64 -AdpGetTime –aALL 【显示适配器时间】
#/opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aAll 【显示所有适配器信息】
#/opt/MegaRAID/MegaCli/MegaCli64 -LDInfo -LALL -aAll 【显示所有逻辑磁盘组信息】
#/opt/MegaRAID/MegaCli/MegaCli64 -PDList -aAll 【显示所有的物理信息】
#/opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuStatus -aALL |grep ‘Charger Status’ 【查看充电状态】
#/opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuStatus -aALL【显示BBU状态信息】
#/opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuCapacityInfo -aALL【显示BBU容量信息】
#/opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuDesignInfo -aALL 【显示BBU设计参数】
#/opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuProperties -aALL 【显示当前BBU属性】
#/opt/MegaRAID/MegaCli/MegaCli64 -cfgdsply -aALL 【显示Raid卡型号，Raid设置，Disk相关信息】
```


## 磁盘分区查看相关命令

**什么是分区**

分区就是将一个物理的磁盘，按照一定的容量划分为多个逻辑的磁盘，每个逻辑磁盘可以叫做一个分区。

**分区的好处**

- 有效防止数据丢失，分区损坏不影响其他分区的数据。

- 增加磁盘空间使用效率：可以用不同的区块大小来格式化分区，如果有很多1K的文件，而硬盘分区区块大小为4K，那么每存储一个文件将会浪费3K空间。这时我们需要取这些文件大小的平均值进行区块大小的划分。

- 将数据分区和系统分区分开，可防止应分区满而导致系统挂起问题；


### df 

可获取硬盘分区占用空间情况。

**常用参数**

```
用法：df [options]
参数：
    -a或--all：包含全部的文件系统；
    --block-size=<区块大小>：以指定的区块大小来显示区块数目；
    -h或--human-readable：以可读性较高的方式来显示信息；
    -H或--si：与-h参数相同，但在计算时是以1000 Bytes为换算单位而非1024 Bytes；
    -i或--inodes：显示inode的信息；
    -k或--kilobytes：指定区块大小为1024字节；
    -l或--local：仅显示本地端的文件系统；
    -m或--megabytes：指定区块大小为1048576字节；
    --no-sync：在取得磁盘使用信息前，不要执行sync指令，此为预设值；
    -P或--portability：使用POSIX的输出格式；
    --sync：在取得磁盘使用信息前，先执行sync指令；
    -t<文件系统类型>或--type=<文件系统类型>：仅显示指定文件系统类型的磁盘信息；
    -T或--print-type：显示文件系统的类型；
    -x<文件系统类型>或--exclude-type=<文件系统类型>：不要显示指定文件系统类型的磁盘信息；
    --help：显示帮助；
    --version：显示版本信息。
```

### du 

du 也是查看使用空间的命令，但是他更多是关注目录和文件使用的空间查看。注意一点，当文件句柄被进程占用时，即使我们把文件删除了，虽然磁盘空间释放了，但是使用`du`查看任然占用，需要重启进程来释放文件句柄，`du`查看才会准确。


```
用法： du [选项][文件]
常用参数：
    -a或-all 显示目录中个别文件的大小。
    -b或-bytes 显示目录或文件大小时，以byte为单位。
    -c或--total 除了显示个别目录或文件的大小外，同时也显示所有目录或文件的总和。
    -k或--kilobytes 以KB(1024bytes)为单位输出。
    -m或--megabytes 以MB为单位输出。
    -s或--summarize 仅显示总计，只列出最后加总的值。
    -h或--human-readable 以K，M，G为单位，提高信息的可读性。
    -x或--one-file-xystem 以一开始处理时的文件系统为准，若遇上其它不同的文件系统目录则略过。
    -L<符号链接>或--dereference<符号链接> 显示选项中所指定符号链接的源文件大小。
    -S或--separate-dirs 显示个别目录的大小时，并不含其子目录的大小。
    -X<文件>或--exclude-from=<文件> 在<文件>指定目录或文件。
    --exclude=<目录或文件> 略过指定的目录或文件。
    -D或--dereference-args 显示指定符号链接的源文件大小。
    -H或--si 与-h参数相同，但是K，M，G是以1000为换算单位。
    -l或--count-links 重复计算硬件链接的文件。

```

### fdisk 

`fdisk` 可以查看物理磁盘分区情况，也可以用来做分区操作。

```
用法: fdisk [选项][设备文件]
参数:
    -b<分区大小>：指定每个分区的大小；
    -l：列出指定的外围设备的分区表状况；
    -s<分区编号>：将指定的分区大小输出到标准输出上，单位为区块；
    -u：搭配"-l"参数列表，会用分区数目取代柱面数目，来表示每个分区的起始地址；
    -v：显示版本信息。
```

系统维护中，常使用 `fdisk -l` 命令来查看分区情况。fdisk的分区功能的使用，是采用问答式的命令行交互，因为它涉及到系统分区情况，操作时一定要认真仔细。[fdisk分区实例](http://man.linuxde.net/fdisk) 是一个简单的分区过程，可作为参考。

### mount 

磁盘分区后，需要使用该命令挂载分区才能使用。除此之外，也常用来挂载CDROM。

```
用法： mount(选项)(设备文件名/加载点)
常用参数：
    -V：显示程序版本；
    -l：显示已加载的文件系统列表；
    -h：显示帮助信息并退出；
    -v：冗长模式，输出指令执行的详细信息；
    -n：加载没有写入文件“/etc/mtab”中的文件系统；
    -r：将文件系统加载为只读模式；
    -a：加载文件“/etc/fstab”中描述的所有文件系统。
```

**实例**

```
# 挂载分区 /dev/sdb1 到 /data1挂载点
mount /dev/sdb1 /data1

# 挂载cdrom 
mount -t auto /dev/cdrom /mnt/cdrom

```

### umount 

类似mount，是卸载挂载点。

```
用法： umount (选项)（文件系统）
参数：
    -a：卸除/etc/mtab中记录的所有文件系统；
    -h：显示帮助；
    -n：卸除时不要将信息存入/etc/mtab文件中；
    -r：若无法成功卸除，则尝试以只读的方式重新挂入文件系统；
    -t<文件系统类型>：仅卸除选项中所指定的文件系统；
    -v：执行时显示详细的信息；
    -V：显示版本信息。

```

**实例**

```
# 卸载分区 /dev/sda1
umount -v /dev/sda1  # 通过设备名
umount -v /data1  # 通过挂载点
# 执行延迟卸载，有时候磁盘被占用，卸载失败时，可使用此方式
umount -vl /data1/     
```

## 参考 

- [https://zh.wikipedia.org/wiki/%E7%A1%AC%E7%9B%98](https://zh.wikipedia.org/wiki/%E7%A1%AC%E7%9B%98)
- [https://zh.wikipedia.org/wiki/%E5%9B%BA%E6%80%81%E7%A1%AC%E7%9B%98](https://zh.wikipedia.org/wiki/%E5%9B%BA%E6%80%81%E7%A1%AC%E7%9B%98)