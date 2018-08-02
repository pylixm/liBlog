# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from .views import IndexView

urlpatterns = [
    url(r'', IndexView.as_view(), name='tutorial_index'),
]
