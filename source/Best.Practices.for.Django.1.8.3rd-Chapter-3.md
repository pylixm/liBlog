---
layout : post
title : Django 最佳实践-读书笔记 - 第三章 如何布局 django 项目
category : django
date : 2016-05-22
tags : [django]
---

[其他章节索引页](2016-05-22-Best.Practices.for.Django.1.8.3rd-Index.html)


# 第三章 如何布局 django 项目

## 建议布局 


```
<repository_root>/
    <django_project_root>/
        <configuration_root>/
```

- `repository_root`  本层放置文件：
  - README.rst
  - docs/
  - directory
  - .gitignore
  - requirements.txt
  
- `django_project_root` 本目录是django项目根目录
- `configuration_root` django项目配置目录
<!-- more -->
```python
icecreamratings_project/
    .gitignore
    Makefile
    docs/
    README.rst
    requirements.txt
    icecreamratings/
        manage.py
        media/ # Development ONLY!
        products/
        profiles/
        ratings/
        static/
        templates/
        config/
            __init__.py
            settings/
            urls.py
            wsgi.py
```

**扩展：**

推荐的 cookiecutter 生成的项目目录：

```
mysite
├── config
│   ├── __init__.py
│   ├── settings
│   │   ├── common.py
│   │   ├── __init__.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── CONTRIBUTORS.txt
├── docs
│   ├── conf.py
│   ├── deploy.rst
│   ├── docker_ec2.rst
│   ├── index.rst
│   ├── __init__.py
│   ├── install.rst
│   ├── make.bat
│   └── Makefile
├── env.example
├── LICENSE
├── manage.py
├── mysite
│   ├── contrib
│   │   ├── __init__.py
│   │   └── sites
│   │       ├── __init__.py
│   │       └── migrations
│   │           ├── 0001_initial.py
│   │           ├── 0002_set_site_domain_and_name.py
│   │           └── __init__.py
│   ├── __init__.py
│   ├── static
│   │   ├── css
│   │   │   └── project.css
│   │   ├── fonts
│   │   ├── images
│   │   │   └── favicon.ico
│   │   ├── js
│   │   │   └── project.js
│   │   └── sass
│   │       └── project.scss
│   ├── templates
│   │   ├── 404.html
│   │   ├── 500.html
│   │   ├── account
│   │   │   ├── base.html
│   │   │   ├── email_confirmed.html
│   │   │   ├── email_confirm.html
│   │   │   ├── email.html
│   │   │   ├── login.html
│   │   │   ├── logout.html
│   │   │   ├── password_change.html
│   │   │   ├── password_reset_done.html
│   │   │   ├── password_reset_from_key_done.html
│   │   │   ├── password_reset_from_key.html
│   │   │   ├── password_reset.html
│   │   │   ├── password_set.html
│   │   │   ├── signup_closed.html
│   │   │   ├── signup.html
│   │   │   ├── verification_sent.html
│   │   │   └── verified_email_required.html
│   │   ├── base.html
│   │   ├── pages
│   │   │   ├── about.html
│   │   │   └── home.html
│   │   └── users
│   │       ├── user_detail.html
│   │       ├── user_form.html
│   │       └── user_list.html
│   └── users
│       ├── adapters.py
│       ├── admin.py
│       ├── __init__.py
│       ├── migrations
│       │   ├── 0001_initial.py
│       │   └── __init__.py
│       ├── models.py
│       ├── tests
│       │   ├── factories.py
│       │   ├── __init__.py
│       │   ├── test_admin.py
│       │   ├── test_models.py
│       │   └── test_views.py
│       ├── urls.py
│       └── views.py
├── pytest.ini
├── README.rst
├── requirements
│   ├── base.txt
│   ├── local.txt
│   ├── production.txt
│   └── test.txt
├── setup.cfg
└── utility
    ├── install_os_dependencies.sh
    ├── install_python_dependencies.sh
    ├── requirements.apt
    └── requirements.apt.xenial

```

