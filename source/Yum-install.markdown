---
layout : post
title : "yum install Header V3 RSA/SHA256 Signature, key ID 0608b895: NOKEY"
category : QA
date : 2015-12-14
tags : [yum ]
---



### Q & A：

使用 yum 安装软件是出现以下错误：


``` bash
	Total size: 8.3 M
	Is this ok [y/N]: y
	Downloading Packages:
	warning: rpmts_HdrFromFdno: Header V3 RSA/SHA256 Signature, key ID 0608b895: NOKEY
	Public key for openpgm-5.1.118-3.el6.x86_64.rpm is not installed
```

原因，这是由于yum安装了旧版本的GPG key或者key文件不存在s造成的
<!-- more -->
### 解决方案：

第一种方式：
使用如下命令导入

```bash
	rpm --import /etc/pki/rpm-gpg/RPM* 
```
如果这种方式不行，用下面的方式：

```bash
	vim /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL
```

使用上门的命令打开文件，并把下面的代码粘贴到文件中。
	
```bash
	-----BEGIN PGP PUBLIC KEY BLOCK-----
	Version: GnuPG v1.2.6 (GNU/Linux)
	
	mQGiBEXopTIRBACZDBMOoFOakAjaxw1LXjeSvh/kmE35fU1rXfM7T0AV31NATCLF
	l5CQiNDA4oWreDThg2Bf6+LIVTsGQb1V+XXuLak4Em5yTYwMTVB//4/nMxQEbpl/
	QB2XwlJ7EQ0vW+kiPDz/7pHJz1p1jADzd9sQQicMtzysS4qT2i5A23j0VwCg1PB/
	lpYqo0ZhWTrevxKMa1n34FcD/REavj0hSLQFTaKNLHRotRTF8V0BajjSaTkUT4uk
	/RTaZ8Kr1mTosVtosqmdIAA2XHxi8ZLiVPPSezJjfElsSqOAxEKPL0djfpp2wrTm
	l/1iVnX+PZH5DRKCbjdCMLDJhYap7YUhcPsMGSeUKrwmBCBJUPc6DhjFvyhA9IMl
	1T0+A/9SKTv94ToP/JYoCTHTgnG5MoVNafisfe0wojP2mWU4gRk8X4dNGKMj6lic
	vM6gne3hESyjcqZSmr7yELPPGhI9MNauJ6Ob8cTR2T12Fmv9w03DD3MnBstR6vhP
	QcqZKhc5SJYYY7oVfxlSOfF4xfwcHQKoD5TOKwIAQ6T8jyFpKbQkRmVkb3JhIEVQ
	RUwgPGVwZWxAZmVkb3JhcHJvamVjdC5vcmc+iGQEExECACQFAkXopTICGwMFCRLM
	AwAGCwkIBwMCAxUCAwMWAgECHgECF4AACgkQEZzANiF1IfabmQCgzvE60MnHSOBa
	ZXXF7uU2Vzu8EOkAoKg9h+j0NuNom6WUYZyJQt4zc5seuQINBEXopTYQCADapnR/
	blrJ8FhlgNPl0X9S3JE/kygPbNXIqne4XBVYisVp0uzNCRUxNZq30MpY027JCs2J
	nL2fMpwvx33f0phU029vrIZKA3CmnnwVsjcWfMJOVPBmVN7m5bGU68F+PdRIcDsl
	PMOWRLkTBZOGolLgIbM4719fqA8etewILrX6uPvRDwywV7/sPCFpRcfNNBUY+Zx3
	5bf4fnkaCKxgXgQS3AT+hGYhlzIqQVTkGNveHTnt4SSzgAqR9sSwQwqvEfVtYNeS
	w5rDguLG41HQm1Hojv59HNYjH6F/S1rClZi21bLgZbKpCFX76qPt8CTw+iQLBPPd
	yoOGHfzyp7nsfhUrAAMFB/9/H9Gpk822ZpBexQW4y3LGFo9ZSnmu+ueOZPU3SqDA
	DW1ovZdYzGuJTGGM9oMl6bL8eZrcUBBOFaWge5wZczIE3hx2exEOkDdvq+MUDVD1
	axmN45q/7h1NYRp5GQL2ZsoV4g9U2gMdzHOFtZCER6PP9ErVlfJpgBUCdSL93V4H
	Sgpkk7znmTOklbCM6l/G/A6q4sCRqfzHwVSTiruyTBiU9lfROsAl8fjIq2OzWJ2T
	P9sadBe1llUYaow7txYSUxssW+89avct35gIyrBbof5M+CBXyAOUaSWmpM2eub24
	0qbqiSr/Y6Om0t6vSzR8gRk7g+1H6IE0Tt1IJCvCAMimiE8EGBECAA8FAkXopTYC
	GwwFCRLMAwAACgkQEZzANiF1IfZQYgCgiZHCv4xb+sTHCn/otc1Ovvi/OgMAnRXY
	bbsLFWOfmzAnNIGvFRWy+YHi
	=MMNL
	-----END PGP PUBLIC KEY BLOCK-----
```