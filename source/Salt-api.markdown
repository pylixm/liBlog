---
layout : post
title : "SaltStack学习笔记2-- salt-api安装配置(转载)"
category : salt
date : 2015-12-15
tags : [salt]
---

原文地址：http://www.xiaomastack.com/2014/11/18/salt-api/

salt-api也用了一段时间了，现在从安装、配置、使用三个方面梳理下知识。
<!-- more -->
## 安装

采用pip安装方便快捷，当然编译安装也很nice。

安装pip采用的编译安装的方式，版本当前最新1.5.6，下载、解压、编译、安装是不变的法则。
    
    [root@saltstack ~]#wget https://pypi.python.org/packages/source/p/pip/pip-1.5.6.tar.gz#md5=01026f87978932060cc86c1dc527903e --no-check-certificate
    [root@saltstack ~]#tar xvfz pip-1.5.6.tar.gz
    [root@saltstack ~]#cd pip-1.5.6
    [root@saltstack pip-1.5.6]#python setup.py build
    [root@saltstack pip-1.5.6]#python setup.py install
    #安装完成后可以用pip freeze查看已安装的packages
    [root@saltstack pip-1.5.6]#pip freeze
    安装CherryPy，版本3.2.3
    
    [root@saltstack ~]#pip install cherrypy==3.2.3
    安装salt-api，版本0.8.3
    
    [root@saltstack ~]#pip install salt-api==0.8.3
    

## 配置
    
    [root@saltstack ~]# cd /etc/pki/tls/certs
    [root@saltstack certs]# make testcert
    umask 77 ; \
        /usr/bin/openssl genrsa -aes128 2048 > /etc/pki/tls/private/localhost.key
    Generating RSA private key, 2048 bit long modulus
    ...+++
    ..................................................................+++
    e is 65537 (0x10001)
    Enter pass phrase:    #键入加密短语，4到8191个字符
    Verifying - Enter pass phrase:    #确认加密短语
    umask 77 ; \
        /usr/bin/openssl req -utf8 -new -key /etc/pki/tls/private/localhost.key -x509 -days 365 -out /etc/pki/tls/certs/localhost.crt -set_serial 0
    Enter pass phrase for /etc/pki/tls/private/localhost.key:    #再次输入相同的加密短语
    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [XX]:CN    #都可以选填
    State or Province Name (full name) []:Shanghai
    Locality Name (eg, city) [Default City]:Shanghai
    Organization Name (eg, company) [Default Company Ltd]:
    Organizational Unit Name (eg, section) []:
    Common Name (eg, your name or your server's hostname) []:
    Email Address []:1989051805@qq.com
    [root@saltstack certs]# cd ../private/
    [root@saltstack private]# openssl rsa -in localhost.key -out localhost_nopass.key
    Enter pass phrase for localhost.key:    #输入之前的加密短语
    writing RSA key
    
如果遇到这样的错误
    
    [root@saltstack certs]# make testcert
    umask 77 ; \
        /usr/bin/openssl req -utf8 -new -key /etc/pki/tls/private/localhost.key -x509 -days 365 -out /etc/pki/tls/certs/localhost.crt -set_serial 0
    unable to load Private Key
    139696733648712:error:0906D06C:PEM routines:PEM_read_bio:no start line:pem_lib.c:703:Expecting: ANY PRIVATE KEY
    make: *** [/etc/pki/tls/certs/localhost.crt]
    
删掉文件/etc/pki/tls/private/localhost.key文件，然后再make testcert。

为salt-api创建用户并设定密码，用户名没有特别要求，我就用saltapi好了。
    
    [root@saltstack ~]#useradd -M -s /sbin/nologin saltapi
    #由于是测试，故采用了弱密码"password"，正式环境必须采用强密码，多用特殊字符
    [root@saltstack ~]# passwd saltapi
    
新增加配置文件/etc/salt/master.d/api.conf和/etc/salt/master.d/eauth.conf
    
    #该配置文件给予saltapi用户所有模块使用权限，出于安全考虑一般只给予特定模块使用权限
    [root@saltstack master.d]# cat eauth.conf
    external_auth:
      pam:
        saltapi:
          - .*
    [root@saltstack master.d]#
    [root@saltstack master.d]# cat api.conf
    rest_cherrypy:
      port: 8888
      ssl_crt: /etc/pki/tls/certs/localhost.crt
      ssl_key: /etc/pki/tls/private/localhost_nopass.key
    [root@saltstack master.d]#
    
寻找salt-api的启动脚本，我比较懒就不自己写了,在页面https://github.com/saltstack/salt-api/releases下载salt-api的tar.gz包,启动脚本在解压包的这个位置./pkg/rpm/salt-api。

不过提供的脚本貌似有个小的bug，就是使用restart参数时，salt-api能够stop但是不能start，如下：
    
    [root@saltstack ~]# /etc/init.d/salt-api restart
    Stopping salt-api daemon:                                  [确定]
    Starting salt-api daemon:                                  [失败]
    
我估计可能是有些相关资源在下次启动前没有来得及释放造成的，解决方法很简单在脚本的restart函数的stop和start之间加上sleep语句。
    
    restart() {
       stop
       sleep 1
       start
    }
    
然后重启就没有问题了
    
    [root@saltstack ~]# /etc/init.d/salt-api restart
    Stopping salt-api daemon:                                  [确定]
    Starting salt-api daemon:                                  [确定]
    [root@saltstack ~]#
    
最后重启salt-master在启动salt-api并将salt-api加入开机启动，安装就完成了。
    
    [root@saltstack ~]# chkconfig salt-api on
    [root@saltstack ~]# /etc/init.d/salt-master restart
    Stopping salt-master daemon:                               [确定]
    Starting salt-master daemon:                               [确定]
    [root@saltstack ~]# /etc/init.d/salt-api restart
    Stopping salt-api daemon:                                  [确定]
    Starting salt-api daemon:                                  [确定]
    [root@saltstack ~]#
    
## 使用（基本的使用方法）

登录获取token
    
    [root@syndic02 ~]# curl -k https://192.168.186.134:8888/login -H "Accept: application/x-yaml" -d username='saltapi' -d password='password' -d eauth='pam'
    return:
    - eauth: pam
      expire: 1416324685.2597771
      perms:
      - .*
      start: 1416281485.2597761
      token: 6171a922a9718ccb40e94ee7c8eb8768f4eea4e5
      user: saltapi
      
获取token后就可以使用token通信
    
    #相当于在salt-master本地执行salt \* test.ping
    [root@syndic02 ~]# curl -k https://192.168.186.134:8888/ -H "Accept: application/x-yaml" -H "X-Auth-Token: 6171a922a9718ccb40e94ee7c8eb8768f4eea4e5" -d client='local' -d tgt='*' -d fun='test.ping'
    return:
    - syndic01: true
      syndic01-minion02: true
      syndic02: true
      syndic02-minion02: true
     
    #相当于在salt-master本地执行salt \* test.echo 'hello world'
    [root@syndic02 ~]# curl -k https://192.168.186.134:8888/ -H "Accept: application/x-yaml" -H "X-Auth-Token: 6171a922a9718ccb40e94ee7c8eb8768f4eea4e5" -d client='local' -d tgt='*' -d fun='test.echo' -d arg='hello world'
    return:
    - syndic01: hello world
      syndic01-minion02: hello world
      syndic02: hello world
      syndic02-minion02: hello world
    [root@syndic02 ~]#
    
运维开发这样使用还是不方便的，下面写的是一个salt-api的类(其它的文章也提到过)可以参考。
    
    #!/usr/bin/env python
    #coding=utf-8
     
    import urllib2, urllib, json, re
     
    class saltAPI:
        def __init__(self):
            self.__url = 'https://192.168.186.134:8888'       #salt-api监控的地址和端口如:'https://192.168.186.134:8888'
            self.__user =  'saltapi'             #salt-api用户名
            self.__password = 'password'          #salt-api用户密码
            self.__token_id = self.salt_login()
     
        def salt_login(self):
            params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
            encode = urllib.urlencode(params)
            obj = urllib.unquote(encode)
            headers = {'X-Auth-Token':''}
            url = self.__url + '/login'
            req = urllib2.Request(url, obj, headers)
            opener = urllib2.urlopen(req)
            content = json.loads(opener.read())
            try:
                token = content['return'][0]['token']
                return token
            except KeyError:
                raise KeyError
     
        def postRequest(self, obj, prefix='/'):
            url = self.__url + prefix
            headers = {'X-Auth-Token'   : self.__token_id}
            req = urllib2.Request(url, obj, headers)
            opener = urllib2.urlopen(req)
            content = json.loads(opener.read())
            return content['return']
     
        def saltCmd(self, params):
            obj = urllib.urlencode(params)
            obj, number = re.subn("arg\d", 'arg', obj)
            res = self.postRequest(obj)
            return res
     
    def main():
        #以下是用来测试saltAPI类的部分
        sapi = saltAPI()
        params = {'client':'local', 'fun':'test.ping', 'tgt':'*'}
        #params = {'client':'local', 'fun':'test.ping', 'tgt':'某台服务器的key'}
        #params = {'client':'local', 'fun':'test.echo', 'tgt':'某台服务器的key', 'arg1':'hello'}
        #params = {'client':'local', 'fun':'test.ping', 'tgt':'某组服务器的组名', 'expr_form':'nodegroup'}
        test = sapi.saltCmd(params)
        print test
     
    if __name__ == '__main__':
        main()
        
测试效果
    
    [root@syndic02 ~]# python salt-api.py
    [{u'syndic02': True, u'syndic02-minion02': True, u'syndic01': True, u'syndic01-minion02': True}]
    [root@syndic02 ~]#
    
以上只是一些基本的实例，salt-api还可以实现更多功能。

## 2016-5-30 update：

当前salt版本：`2016.3`，官网对salt各模块安装配置文档做了整理重拍，更加清晰明了。

前段时间试着按官方的文档搭建了下salt环境，感觉安装更简单了，下面更新下 salt-api的安装：

    # https://docs.saltstack.com/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html
    # 1、安装 salt-api 
    yum install salt-api 
    
    # 2、生成 https ssl 证书
    salt-call --local tls.create_self_signed_cert
    
    # 3、向master 配置文件中增加：
    rest_cherrypy:
    port: 8000
    ssl_crt: /etc/pki/tls/certs/localhost.crt
    ssl_key: /etc/pki/tls/certs/localhost.key
    
    # 4、创建salt 用户
    [root@saltstack ~]# useradd -M -s /sbin/nologin salt
    [root@saltstack ~]# passwd salt
    # 修改 master 配置信息
    external_auth:
      pam:
        saltapi:
          - .*  
    # 5、增加 api 访问信息
     rest_cherrypy:
       port: 8888
       ssl_crt: /etc/pki/tls/certs/localhost.crt
       ssl_key: /etc/pki/tls/private/localhost_nopass.key

到此，salt-api 安装配置完成。需要注意的是，有时候 yum 和 pip 使用的python 并不是一个，所以有些依赖包安装的时候，尽量统一使用一种包管理管理工具。
    