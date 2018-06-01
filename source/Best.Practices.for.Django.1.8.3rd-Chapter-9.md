---
layout : post
title : Django 最佳实践-读书笔记 - 第十一章、第十二章 Form 
category : django
date : 2016-06-26 20:16:00
tags : [django]
---

[其他章节索引页](2016-05-22-Best.Practices.for.Django.1.8.3rd-Index.html)

# 第十一章 Form 

## 所有录入的数据使用form 来进行校验

面对复杂多变的需求，我们自行校验是比较困难的。将校验集中在form层，利用这久经考验的校验机制。

## 在 html 的form 中使用 post方法，除了查询。

## 在使用http的form形式来修改数据时，记得使用 csrf来保护数据。

除了 http 的形式外，ajax 提交的也要使用csrf 来保护数据。

## 理解怎么给 form 实例添加属性

```python 
# forms
from django import forms
from .models import Taster


class TasterForm(forms.ModelForm):
    class Meta:
        model = Taster
        
    def __init__(self, *args, **kwargs):
        # set the user as an attribute of the form
        self.user = kwargs.pop('user')
        super(TasterForm, self).__init__(*args, **kwargs)
```

```python 
# views
from django.views.generic import UpdateView
from braces.views import LoginRequiredMixin
from .forms import TasterForm
from .models import Taster

class TasterUpdateView(LoginRequiredMixin, UpdateView):
    model = Taster
    form_class = TasterForm
    success_url = "/someplace/"
    
    def get_form_kwargs(self):
        """This method is what injects forms with their keyword arguments."""
        # grab the current set of form #kwargs
        kwargs = super(TasterUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs
.

```

## 知道 form 校验是怎么工作的

当你调用 `form.is valid()`时，很多事情发生：

- 如果这个form已经绑定了数据，``form.is_valid()`会调用 `form.full_clean()` 方法。
- `form.full_clean()` 方法会遍历form 的字段，挨个字段的校验他们。
  - 进入字段的数据会通过 `to_python()`方法被强制转为python格式，否则会抛出`ValidationError`异常。
  - 数据针对每个字段特有的规则或自定义的规则，进行校验。失败后，抛出`ValidationError`异常。
  - 如果有自定的`clean <field>()`方法，此时会调用他们
- `form.full_clean()` 会执行 `form.clean()`方法。
- 如果是一个`ModelForm`实例,`form.post_clean()`会如下处理：
  - 将 `ModelForm` 数据转成 `Model` 实例，而不管 `form.is_valid()` 是否严重通过。
  - Calls the model’s clean() method. For reference, saving a model instance through the
ORM does not call the model’s clean() method.

## 一些有用的 form 方法 

- Add Errors to Forms with Form.add error()
- http://www.2scoops.co/1.8-form.errors.as_data/
- http://www.2scoops.co/1.8-form.errors.as_json/
- http://www.2scoops.co/1.8-form.has_error/
- http://www.2scoops.co/1.8-form.non_field_errors/


# 第 十二 章 Form 通用的技巧

## 简单的 `ModelForm` 使用默认的校验即可。

```python
# flavors/views.py
from django.views.generic import CreateView, UpdateView
from braces.views import LoginRequiredMixin
from .models import Flavor


class FlavorCreateView(LoginRequiredMixin, CreateView):
    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')
    
    
class FlavorUpdateView(LoginRequiredMixin, UpdateView):
    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')
```

## 自定义字段验证,进行特定的校验

```python
# core/validators.py
from django.core.exceptions import ValidationError

def validate_tasty(value):
    """Raise a ValidationError if the value doesn't start with the
    word 'Tasty'.
    """
    if not value.startswith(u"Tasty"):
        msg = u"Must start with Tasty"
        raise ValidationError(msg)
        
# 直接将校验添加到 model中
# core/models.py
from django.db import models
from .validators import validate_tasty

class TastyTitleAbstractModel(models.Model):
    title = models.CharField(max_length=255, validators=[validate_tasty])
    class Meta:
        abstract = True
        
# flavors/models.py
from django.core.urlresolvers import reverse
from django.db import models
from core.models import TastyTitleAbstractModel

class Flavor(TastyTitleAbstractModel):
    slug = models.SlugField()
    scoops_remaining = models.IntegerField(default=0)
    def get_absolute_url(self):
        return reverse("flavors:detail", kwargs={"slug": self.slug})
        
# 仅将校验添加到form 中    
# flavors/forms.py
from django import forms
from core.validators import validate_tasty
from .models import Flavor

class FlavorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
    super(FlavorForm, self).__init__(*args, **kwargs)
    self.fields["title"].validators.append(validate_tasty)
    self.fields["slug"].validators.append(validate_tasty)
    class Meta:
        model = Flavor
```

## Overriding the Clean Stage of Validation

原因：

- 对多`Multi-field` 的校验
- 避免重复验证（Validation involving existing data from the database that has already been validated）

```python
# flavors/forms.py
from django import forms
from flavors.models import Flavor

class IceCreamOrderForm(forms.Form):
    """Normally done with forms.ModelForm. But we use forms.Form here
    to demonstrate that these sorts of techniques work on every
    type of form.
    """
    slug = forms.ChoiceField("Flavor")
    toppings = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super(IceCreamOrderForm, self).__init__(*args,
        **kwargs)
        # We dynamically set the choices here rather than
        # in the flavor field definition. Setting them in
        # the field definition means status updates won't
        # be reflected in the form without server restarts.
        self.fields["slug"].choices = [
        (x.slug, x.title) for x in Flavor.objects.all()
        ]
        # NOTE: We could filter by whether or not a flavor
        # has any scoops, but this is an example of
        # how to use clean_slug, not filter().
        
    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        if Flavor.objects.get(slug=slug).scoops_remaining <= 0:
            msg = u"Sorry, we are out of that flavor."
            raise forms.ValidationError(msg)
        return slug

    def clean(self):
        cleaned_data = super(IceCreamOrderForm, self).clean()
        slug = cleaned_data.get("slug", "")
        toppings = cleaned_data.get("toppings", "")
        
        # Silly "too much chocolate" validation example
        if u"chocolate" in slug.lower() and \
            u"chocolate" in toppings.lower():
            msg = u"Your order has too much chocolate."
            raise forms.ValidationError(msg)
        return cleaned_data
```

## 扩展 `Django Form Field` (2 CBVs, 2 Forms, 1 Model)

2个 view，2个form 对应一个model

```python
# stores/models.py
from django.core.urlresolvers import reverse
from django.db import models

class IceCreamStore(models.Model):
    title = models.CharField(max_length=100)
    block_address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    
    def get_absolute_url(self):
        return reverse("store_detail", kwargs={"pk": self.pk})
        
# stores/forms.py
# Call phone and description from the self.fields dict-like object
from django import forms
from .models import IceCreamStore
class IceCreamStoreUpdateForm(forms.ModelForm):

    class Meta:
        model = IceCreamStore
    
    def __init__(self, *args, **kwargs):
        # Call the original __init__ method before assigning
        # field overloads
        super(IceCreamStoreUpdateForm, self).__init__(*args,
        **kwargs)
        self.fields["phone"].required = True
        self.fields["description"].required = True


# stores/forms.py
from django import forms
from .models import IceCreamStore
class IceCreamStoreCreateForm(forms.ModelForm):
    class Meta:
        model = IceCreamStore
        fields = ("title", "block_address", )
        
class IceCreamStoreUpdateForm(IceCreamStoreCreateForm):
    def __init__(self, *args, **kwargs):
        super(IceCreamStoreUpdateForm,
        self).__init__(*args, **kwargs)
        self.fields["phone"].required = True
        self.fields["description"].required = True
    class Meta(IceCreamStoreCreateForm.Meta):
        # show all the fields!
        fields = ("title", "block_address", "phone",
        "description", )
        
# stores/views
from django.views.generic import CreateView, UpdateView
from .forms import IceCreamStoreCreateForm
from .forms import IceCreamStoreUpdateForm
from .models import IceCreamStore
class IceCreamCreateView(CreateView):
    model = IceCreamStore
    form_class = IceCreamStoreCreateForm
class IceCreamUpdateView(UpdateView):
    model = IceCreamStore
    form_class = IceCreamStoreUpdateForm
```

## 在views中，重复使用搜索 mixin 

一个搜索 from 在2个view 中使用。

```python
# core/views.py
class TitleSearchMixin(object):
    def get_queryset(self):
        # Fetch the queryset from the parent's get_queryset
        queryset = super(TitleSearchMixin, self).get_queryset()
        # Get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            # return a filtered queryset
            return queryset.filter(title__icontains=q)
        # No q is specified so we return queryset
        return queryset
        
# add to flavors/views.py
from django.views.generic import ListView
from core.views import TitleSearchMixin
from .models import Flavor
class FlavorListView(TitleSearchMixin, ListView):
    model = Flavor


# add to stores/views.py
from django.views.generic import ListView
from core.views import TitleSearchMixin
from .models import Store
class IceCreamStoreListView(TitleSearchMixin, ListView):
    model = Store
```

```html  
{# form to go into stores/store_list.html template #}
<form action="" method="GET">
<input type="text" name="q" />
<button type="submit">search</button>
</form>

{# form to go into flavors/flavor_list.html template #}
<form action="" method="GET">
<input type="text" name="q" />
<button type="submit">search</button>
</form>
```


# form 相关3方包推荐：

PACKAGE TIP: Useful Form-Related Packages
- `django-floppyforms` for rendering Django inputs in HTML5.
- `django-crispy-forms` for advanced form layout controls. By default, forms are rendered
with Twitter Bootstrap form elements and styles. This package plays well with django-
floppyforms, so they are often used together.
- `django-forms-bootstrap` is a simple tool for rendering Django forms using Twitter
Bootstrap styles. This package plays well with django-floppyforms but con..icts with
django-crispy-forms.