# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from .views import IndexView, PostDetailView, TagView, CategoryView,\
    ArchiveView

urlpatterns = [

    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^post/(?P<slug>\d+)/$', PostDetailView.as_view(),
        name='post-detail'),
    url(r'^tags/$', TagView.as_view(), name='tags'),
    url(r'^tag/(?P<slug>\w+)/$', TagView.as_view(), name='tag'),
    url(r'^categories/$', CategoryView.as_view(), name='categories'),
    url(r'^category/(?P<slug>\w+)/$', CategoryView.as_view(), name='category'),
    url(r'^archive/$', ArchiveView.as_view(), name='archive'),

    # url(r'^post/comments/', include('django_comments.urls')),
    url(r'^comments/', include('django_comments_xtd.urls')),

]
