# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic import View, TemplateView
from django.contrib import admin
from django.conf import settings

admin.site.index_title = 'liBlog Admin'
admin.site.site_header = 'liBlog Admin'
admin.site.site_title = 'liBlog Admin'

handler500 = 'liBlog.blogs.views.server_error'
handler404 = 'liBlog.blogs.views.page_not_found'

urlpatterns = [

    # Django Admin, use {% url 'admin:index' %}
    # url(r'^jet/', include('jet.urls', 'jet')),
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('liBlog.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Third App
    # 上传图片url
    url(r'mdeditor/', include('mdeditor.urls')),

    url(r'^search/', include('haystack.urls', namespace='haystack')),

    # tutorial
    url(r'^tutorial/', include('liBlog.tutorial.urls', namespace='tutorial')),

    # Your stuff: custom urls includes go here
    url(r'', include('liBlog.blogs.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)