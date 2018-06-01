# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Post, Tag, Category

# # 添加blogs models
# myapp = apps.get_app_config('blogs')
# for model in myapp.get_models():
#     admin.site.register(model)


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish_time', 'category', 'status',
                    'view_count', 'update_time']
    search_fields = ['title', 'category__name']


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)