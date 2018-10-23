---
layout : post
title : 译-Django restfull framework 中API版本的管理
category : django
date : 2017-04-24 
tags : [django, restfull, 翻译]
---

>原文：https://gearheart.io/blog/api-versioning-with-django-rest-framework/

## 什么情况下会有多版本的 api 的需求

我们在升级服务的时候，通常是向后兼容的。这样我们在升级客户端代码的时候，便不会遇到太大的困难。然而，当移动端的api升级后，客户手机中的app客户端有可能不会升级，所以我们必须保证所有版本的API的正常运行。

一个系统应该有一个好的api版本控制：新的功能和更改应该在新的版本中。旧的客户端可以使用旧的API，新的客户端可以使用新版本的API。
<!-- more -->
## DRF 中支持的版本管理方案

DRF中支持多种版本管理方案。

### AcceptHeaderVersioning

通过接受请求标头传递版本号：
```
GET /bookings/ HTTP/1.1
Host: example.com
Accept: application/json; version=1.0
```

### URLPathVersioning

将版本以变量的方式添加到url地址（通过VERSION_PARAM参数在DRF中指定路径）：
```
urlpatterns = [
    url(
        r'^(?P<version>(v1|v2))/bookings/$',
        bookings_list,
        name='bookings-list'
    )
]
```

### NamespaceVersioning

通过 url namespace 来区分版本：
```
# urls.py
urlpatterns = [
    url(r'^v1/bookings/', include('bookings.urls', namespace='v1')),
    url(r'^v2/bookings/', include('bookings.urls', namespace='v2'))
]
```

### HostNameVersioning

通过域名来设置版本：
```
http://v1.example.com/bookings/
http://v2.example.com/bookings/
```

### QueryParameterVersioning

通过 get query string 参数来专递版本：
```
http://example.com/bookings/?version=0.1
http://example.com/bookings/?version=0.2
```

## DRF 中版本化代码 

在DRF 文档中介绍了第一个版本控制的方法。如下：

创建 Serializer 和 ViewSet 
```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'users', 'created')


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
```

如果我们需要更改/删除/添加一个字段，我们创建一个新的序列化程序并更改其中的字段。
```python
class AccountSerializerVersion1(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'users', 'created', 'updated')
```

然后我们在AccountViewSet中重新定义get_serializer_class方法：
```python
def get_serializer_class(self):
    if self.request.version == 'v1':
        return AccountSerializerVersion1
    return AccountSerializer
```

这是在ViewSet中重新定义序列化程序，权限类和其他方法的一种方法。

同时，我发现一个小的版本控制的[项目](https://github.com/mrhwick/django-rest-framework-version-transforms)。

我没有使用它，但是从文档中我们可以设置Serializer和Parser并使用它们来设置变换的基类。
```python
from rest_framework_transforms.transforms import BaseTransform

class TestModelTransform0002(BaseTransform):
    """
    Changes between v1 and v2
    """
    def forwards(self, data, request):
        if 'test_field_one' in data:
            data['new_test_field'] = data.get('test_field_one')
            data.pop('test_field_one')
        return data

    def backwards(self, data, request, instance):
        data['test_field_one'] = data.get('new_test_field')
        data.pop('new_test_field')
        return data

```
设置基本版本：
```python
class TestSerializerV3(BaseVersioningSerializer):
    transform_base = 'tests.test_transforms.TestModelTransform'

    class Meta:
        model = TestModelV3
        fields = (
            'test_field_two',
            'test_field_three',
            'test_field_four',
            'test_field_five',
            'new_test_field',
            'new_related_object_id_list',
        )
```
我们这样创建每个新版本：
```python
class TestModelTransform0003(BaseTransform):
    """
    Changes between v2 and v3
    """

    def forwards(self, data, request):
        data['new_related_object_id_list'] = [1, 2, 3, 4, 5]
        return data

    def backwards(self, data, request, instance):
        data.pop('new_related_object_id_list')
        return data
```
从客户端接收数据（即0004，0003，0002）时，向后的方法将从结尾开始应用。向客户端发送数据时，转发将按照0002，0003，0004的顺序进行。


## 我们是如何处理版本的

基本思想是将API分解为模块并使用类继承。

如下目录结构：
```bash
api/
├── base
│   ├── init.py
│   ├── router.py
│   ├── serializers.py
│   └── views.py
├── init.py
└── versioned
    ├── init.py
    ├── v2
    │   ├── init.py
    │   ├── router.py
    │   ├── serializers.py
    │   └── views.py
    ├── v3
    │   ├── init.py
    │   ├── router.py
    │   ├── serializers.py
    │   └── views.py
    ├── v4
    │   ├── init.py
    │   ├── router.py
    │   ├── serializers.py
    │   └── views.py
    └── v5
        ├── init.py
        ├── router.py
        ├── serializers.py
        └── views.py
```

base - 我们的基础版本API，第一个版本。

此外，在版本化文件夹中，我们为每个版本创建了一个文件夹。在这个项目中，我们有两个外部客户：iOS和Android +我们的WEB客户端。 WEB客户端一直使用最新版本的API。

每个连续的API版本是这样处理的：我们在现有的API v2中进行了更改; 在iOS和Android客户端发布之后（他们同时发布），我们创建了v3，并停止对v2进行更改。

DRF使用类来创建ViewSet，Serializer，Permission。我们使用API​​版本之间的继承来完全复制ViewSets和Serializer。
```python
# base/serializers.py

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = 'all'
```

```python
# base/views.py
from . import serializers

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
```

```python
# base/router.py
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'books', views.BookViewSet)

api_urlpatterns = router.urls
```

此外，我们将urls.py连接到第一个API版本：
```python
from .api.base.router import api_urlpatterns as api_v1

urlpatterns = [
    url(r'^api/v1/', include(api_v1)),
]
```

我们删除了first_name，last_name字段并添加了full_name字段。然后我们创建了v2保持向后兼容性，并添加了serializers.py，views.py，router.py目录和文件：
```python
└── versioned
    ├── init.py
    ├── v2
    │   ├── init.py
    │   ├── router.py
    │   ├── serializers.py
    │   └── views.py
```
继承base 版本：
```python
# versioned/v2/serializers.py

# import all our basic serializers

from .api.base import serializers as base_serializers
from .api.base.serializers import *

class UserSerializer(base_serializers.UserSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta(base_serializers.UserSerializer.Meta):
        fields = ('id', 'email', 'full_name')

    def get_full_name(self, obj):
        return '{0} {1}'.format(obj.first_name, obj.last_name)
```

```python
# versioned/v2/views.py
from .api.base.views import *
from .api.base import views as base_views
from . import serializers as v2_serializers


class UserViewSet(base_views.UserViewSet):
    serializer_class = v2_serializers.UserSerializer
```

```python
# versioned/v2/router.py
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'books', views.BookViewSet)

api_urlpatterns = router.urls
```
更新root url 文件：
```python
from .api.base.router import api_urlpatterns as api_v1
from .api.versioned.v2.router import api_urlpatterns as api_v2

urlpatterns = [
    url(r'^api/v1/', include(api_v1)),
    url(r'^api/v2/', include(api_v2)),
]
```
您可能会注意到我们已经继承了UserViewSet，而且我们没有更新BookViewSet，这是因为我们在v2视图视图中引入了base 的视图。

## 以上方法的优缺点

### 优点

- 开发简单
- 相关类的版本由模块基础，v1，v2等分类。
- 易于浏览代码
- 无需复制 view 和 serializers 的源代码。
- 少 if 嵌套

### 缺点

- 当API 版本过多时，会造成代码继承层数多大，不利于维护。
- 应为要继承，需要简单修改部分代码。

## 总结

管理API版本可能相当困难，尤其是要正确实施。您可以在每个版本控制方法中找到优缺点。由于我们项目中的版本少，所以继承方法是比较实用的。


#### 参考： 

- [http://www.django-rest-framework.org/api-guide/versioning/](http://www.django-rest-framework.org/api-guide/versioning/)
- [https://gearheart.io/blog/api-versioning-with-django-rest-framework/](https://gearheart.io/blog/api-versioning-with-django-rest-framework/)