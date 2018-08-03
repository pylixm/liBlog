# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from .views import IndexView, CountView

urlpatterns = [
    url(r'count/$', CountView.as_view(), name='tutorial_count'),
    url(r'$', IndexView.as_view(), name='tutorial_index'),
]
