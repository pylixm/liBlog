---
layout : post
title : Django 最佳实践-读书笔记 - 第八、九、十章 FBVS & CBVS
category : django
date : 2016-06-19 22:30:00
tags : [django]
---


[其他章节索引页](2016-05-22-Best.Practices.for.Django.1.8.3rd-Index.html)

# 第八章 FBVS & CBVS

## 如何选择 function - views 和 class - views 

见流程图：
![](/static/imgs/wtovsyu.png)

## urlconf 中不要包含 views 的逻辑 

```
Bad example :
from django.conf.urls import url
from django.views.generic import DetailView
from tastings.models import Tasting
urlpatterns = [
  url(r"^(?P<pk>\d+)/$",
    DetailView.as_view(
    model=Tasting,
    template_name="tastings/detail.html"),
    name="detail"),
  url(r"^(?P<pk>\d+)/results/$",
    DetailView.as_view(
    model=Tasting,
    template_name="tastings/results.html"),
    name="results"),
]
```
<!-- more -->
优点:

- 在 views 避免了重复的代码
- 松耦合
- url 集中处理路由问题
- views 可以得到 class-based views 的所有优点
- 更加灵活

## 使用url name space 更好的管理 url

`url(r'^detail/', include('tastings.urls', namespace='tastings')),`

通过 `tastings:detail` 调用。 

url设计原则：
- url 尽量短小，明显 
- 更容易搜索，更新，重构

## 不要在url 中使用 string的 views路径

`url(r'^$', 'polls.views.index', name='index'),` 

- 当views 有错误时，导致调试困难
- Instructors have to explain to beginners the need for an empty string at the beginning of the urlpatterns variable。

## 将业务逻辑移除 views 便于管理复用

## 尽量不要使用locals() 作为 Views Context

- 有可能会污染 template 变量环境
- 当变量较多时，消耗不必要的资源


# 第九章 Function-based views 最佳实践

## 编写function-based views 建议

- 保持views 的最小代码量 
- 在views 中不要重复的代码
- views 中保留着表现逻辑，业务逻辑尽可能的在models、form层。
- 使用 function-based views 编写自定义的 错误处理（403, 404, and 500 error handlers.）
- 避免负责逻辑的嵌套。

## 通过 request、response 对象来传递属性值。

## function-based views 可以更好的利用装饰器

# 第十章 Class-based views 最佳实践

## 编写class-based views 建议

- 保持views 的最小代码量 
- 在views 中不要重复的代码
- views 中保留着表现逻辑，业务逻辑尽可能的在models、form层。
- 不要使用class-based views，使用 function-based views 编写自定义的 错误处理（403, 404, and 500 error handlers.）
- 使 mixins 最小化。

## mixins 使用排序： python-object, mixins , base-views 

```
class FruityFlavorView(FreshFruitMixin, TemplateView):
template_name = "fruity_flavor.html"
```

## 什么时候使用什么视图 

|Name | Purpose |Two Scoops Example|
|-----|---------|------------------|
|View | Base view or handy view that can be used foranything.| See section 10.6, `Using Justdjango.views.generic.View'.|
|RedirectView | Redirect user to another URL | Send users who visit `/log-in/' to`/login/'. |
|TemplateView | Display a Django HTML template. | The `/about/' page of our site.|
|ListView     | List objects                    | List of ice cream flavors.
|DetailView   | Display an object | Details on an ice cream flavor.
|FormView     | Submit a form  | The site's contact or email form.
|CreateView   | Create an object | Create a new ice cream flavor.
|UpdateView   | Update an object | Update an existing ice cream flavor.
|DeleteView   | Delete an object | Delete an unpleasant ice cream flavorlike Vanilla Steak.
|Generic date views | For display of objects that occur over a rangeof time.| Blogs are a common reason to usethem. For Two Scoops, we could create a public history of when flavors havebeen added to the database. 


## 使用 LoginRequiredMixin 来进行用户认证

```
class FlavorDetailView(LoginRequiredMixin, DetailView):
    model = Flavor
```
## 将多个视图都需要重写的方法放入到 mixin 中，以保证视图的简单清晰

```
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView
from braces.views import LoginRequiredMixin
from .models import Flavor

class FlavorActionMixin(object):
    fields = ('title', 'slug', 'scoops_remaining')

    @property
    def success_msg(self):
        return NotImplemented
    
    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(FlavorActionMixin, self).form_valid(form)

class FlavorCreateView(LoginRequiredMixin, FlavorActionMixin,
CreateView):
    model = Flavor
    success_msg = "Flavor created!"

class FlavorUpdateView(LoginRequiredMixin, FlavorActionMixin,
UpdateView):
    model = Flavor
    success_msg = "Flavor updated!"

```


ps： 感觉本书views 这里讲的比较乱, 部分class-based views 可参见另一篇博文： [Django class views](http://pylixm.cc/posts/2016-03-24-Django-Classviews.html)

