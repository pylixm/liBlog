# -*- coding:utf-8 -*-
import traceback
import sys
import logging
import datetime

import mistune
from django.http import Http404
from django.shortcuts import render_to_response
from django.db.models import Count
from django.views.generic import View, ListView, DetailView
from django.conf import settings

from .models import *
from .serivce import TocRenderer


logger = logging.getLogger(__name__)


def server_error(request):
    return render_to_response("500.html")


def page_not_found(request):
    return render_to_response("404.html")


# class LoginRequiredMixin(object):
#
#     @classmethod
#     def as_view(cls, **initkwargs):
#         view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
#         return login_required(view)


class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            # 整站信息
            context['site_ext'] = settings.SITE
            # 发布时间
            publish_time = datetime.datetime.strptime(
                settings.SITE.get('publish_time', '2018-05-14 16:00:00'),
                '%Y-%m-%d %H:%M:%S')
            last_publish_time = datetime.datetime.strptime(
                settings.SITE.get('last_publish_time', '2018-05-14 16:00:00'),
                '%Y-%m-%d %H:%M:%S')
            context['site_publish_days'] = (datetime.datetime.now() - publish_time).days
            context['last_publish_days'] = (datetime.datetime.now() - last_publish_time).days
            # 标签
            context['sidbar_tag_list'] = Tag.objects.values('name').annotate(
                post_count=Count('post_list')).filter(
                post_count__gt=settings.TAG_SIDE_SHOW_NUM).order_by('-post_count')
        except Exception as e:
            logger.error(" ".join(traceback.format_exception(*sys.exc_info())))
        return context


class IndexView(BaseMixin, ListView):
    queryset = Post.available_list()
    template_name = 'blogs/index.html'
    # 指定 queryset 的名字
    context_object_name = 'post_list'
    # 列表页 每页显示多少条
    paginate_by = settings.PAGENUM


class PostDetailView(BaseMixin, DetailView):
    model = Post
    template_name = 'blogs/post.html'
    context_object_name = 'post'
    # 可指定作为 文章标识的key 默认为 id
    slug_field = 'id'

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object()
        toc_render = TocRenderer(inlinestyles=True, linenos=True)
        toc_render.reset_toc()
        markdown = mistune.Markdown(renderer=toc_render)
        post.content = markdown.parse(post.content)
        post.toc = toc_render.render_toc()
        return post

    def get(self, request, *args, **kwargs):
        obj = super(PostDetailView, self).get_object()
        obj.view_count += 1
        obj.save()
        return super(PostDetailView, self).get(request, *args, **kwargs)


class TagView(BaseMixin, ListView):
    template_name = 'blogs/tag.html'
    context_object_name = 'tag_list'

    def get_queryset(self):
        tag = self.kwargs.get('slug', '')
        if tag:
            tag_list = Tag.objects.filter(name=tag)
        else:
            tag_list = Tag.objects.values('name').annotate(
                post_count=Count('post_list'))
            for tag in tag_list:
                count = tag['post_count']
                if count < settings.TAG_LEVEL_1:
                    tag['tag_css'] = 1
                elif settings.TAG_LEVEL_1 <= count < settings.TAG_LEVEL_2:
                    tag['tag_css'] = 2
                elif settings.TAG_LEVEL_2 <= count < settings.TAG_LEVEL_3:
                    tag['tag_css'] = 3
                else:
                    tag['tag_css'] = 4
            self.template_name = 'blogs/tags_cloud.html'
        return tag_list


class CategoryView(BaseMixin, ListView):
    template_name = 'blogs/category.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        category = self.kwargs.get('slug', '')
        if category:
            category_list = Category.objects.filter(name=category)
        else:
            category_list = Category.objects.all()
        return category_list


class ArchiveView(BaseMixin, ListView):
    # queryset = Post.archive_list()
    template_name = 'blogs/archive.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        post_list = Post.objects.filter(status=1)
        date = None
        for post in post_list:
            new_date = '{0}-{1}'.format(post.publish_time.year,
                                        str(post.publish_time.month)
                                        .rjust(2, '0'))
            if date is None or new_date != date:
                post.date = new_date
                date = post.date
        return post_list
