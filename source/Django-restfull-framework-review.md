---
layout : post
title : Django restfull framework 学习使用总结-权限相关
category : django
date : 2016-01-08 21:15:00
tags : [django, restfull]
---



### 0X00 默认权限 permissions 的配置说明：

- ``AllowAny``
	
	允许任何人调用

    Allow any access.

- ``IsAuthenticated`` 

	只允许认证用户调用（在django auth表中注册的用户）

    Allows access only to authenticated users.

- ``IsAdminUser`` 

	只允许管理员（即可以登录admin后端的用户，`user.is_staff` is `True` 的用户）

    Allows access only to admin users.

    The IsAdminUser permission class will deny permission to any user, unless `user.is_staff` is `True` in which case permission will be allowed.

- ``IsAuthenticatedOrReadOnly`` 
	
	允许任何只读调用，和认证的用户调用

    The request is authenticated as a user, or is a read-only request.

- ``DjangoModelPermissions``   

	请求认证同django的用户 相关请求 model的权限

    The request is authenticated using `django.contrib.auth` permissions.
    See: https://docs.djangoproject.com/en/dev/topics/auth/#permissions

    It ensures that the user is authenticated, and has the appropriate
    `add`/`change`/`delete` permissions on the model.

    This permission can only be applied against view classes that
    provide a `.model` or `.queryset` attribute.

- ``DjangoModelPermissionsOrAnonReadOnly`` 

	同DjangoModelPermissions
 
    Similar to DjangoModelPermissions, except that anonymous users are
    allowed read-only access.

- ``DjangoObjectPermissions``

	比较少用，需要增加django三方权限库django-guardian.

    The request is authenticated using Django's object-level permissions.
    It requires an object-permissions-enabled backend, such as Django Guardian.

    It ensures that the user is authenticated, and has the appropriate
    `add`/`change`/`delete` permissions on the object using .has_perms.

    This permission can only be applied against view classes that
    provide a `.model` or `.queryset` attribute.

### 0X01 默认认证说明： 

- `BasicAuthentication`

    This authentication scheme uses HTTP Basic Authentication, signed against a user's username and password. Basic authentication is generally only appropriate for testing.
    
    基本的 http 验证，仅验证用户名和密码，仅用于测试使用。
    
- `SessionAuthentication`

    This authentication scheme uses Django's default session backend for authentication. Session authentication is appropriate for AJAX clients that are running in the same session context as your website.
    
    此种认证发难使用 django的默认sesstion方式 。适用于那些在同一个session交互的 ajax 的客户端或网站。
    
- `TokenAuthentication`

    This authentication scheme uses a simple token-based HTTP Authentication scheme. Token authentication is appropriate for client-server setups, such as native desktop and mobile clients.
    
    此验证方案使用一个简单的基于令牌的HTTP认证。令牌认证适用于客户端 - 服务器设置，如本机桌面和移动客户端。


### 0X02 自定义认证和权限
    
#### 认证

继承 `BaseAuthentication` 类并重写 `.authenticate(self, request)` 方法。

[官方例子](http://www.django-rest-framework.org/api-guide/authentication/#example)

#### 权限 

继承 `BasePermission` 类重写 `.has_permission(self, request, view)` 或 `.has_object_permission(self, request, view, obj)` 方法。

[官方例子](http://www.django-rest-framework.org/api-guide/permissions/#examples)

### 0X03 使用方法

方法一 ：

将配置信息放在django的setting文件中：

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        )
    }

方法二：

直接放在接口 views中 
    
    # class 视图
    class ExampleView(APIView):
        authentication_classes = (SessionAuthentication, BasicAuthentication)
        permission_classes = (IsAuthenticated,)

        def get(self, request, format=None):
            content = {
                'user': unicode(request.user),  # `django.contrib.auth.User` instance.
                'auth': unicode(request.auth),  # None
            }
            return Response(content)

    # func 视图
    @api_view(['GET'])
    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((IsAuthenticated,))
    def example_view(request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)



---

#### 参考： 

* [http://www.django-rest-framework.org/api-guide/authentication/](http://www.django-rest-framework.org/api-guide/authentication/)
