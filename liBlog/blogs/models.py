# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from mdeditor.fields import MDTextField


class Post(models.Model):
    DRAFT = 0
    PUBLISH = 1
    REMOVE = 2
    STATUS = {
        DRAFT: u'草稿',
        PUBLISH: u'正常',
        REMOVE: u'删除',
    }
    title = models.CharField(u'标题', max_length=100)
    publish_time = models.DateTimeField(u'发布时间')
    tags = models.ManyToManyField('Tag', verbose_name=u'标签',
                                  related_name='post_list')
    category = models.ForeignKey('Category', verbose_name=u'分类',
                                 related_name='post_list')
    status = models.IntegerField(choices=STATUS.items(), verbose_name=u'状态',
                                 default=0)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True,
                                       editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    summary = models.TextField(u"摘要", default=None)
    content = MDTextField("正文")
    allow_comments = models.BooleanField('allow comments', default=True)
    view_count = models.IntegerField('阅读量', default=0)

    def __str__(self):
        return '%s' % self.title

    def get_tags(self):
        return map(lambda x: x.name, self.tags.all())

    def get_absolute_url(self):
        return '/post/%s/' % (self.id)

    def next_post(self):
        return Post.objects.filter(id__gt=self.id, status=1).order_by(
            'id').first()

    def prev_post(self):
        return Post.objects.filter(id__lt=self.id, status=1).first()

    @classmethod
    def available_list(cls):
        return cls.objects.filter(status=1)

    # @classmethod
    # def archive_list(cls):
    #     post_list = cls.objects.filter(status=1)
    #     year = None
    #     for post in post_list:
    #         if year == None or post.publish_time.year != year:
    #             post.year = post.publish_time.year
    #             year = post.year
    #     return post_list

    class Meta:
        ordering = ['-publish_time']
        verbose_name_plural = u'文章'
        verbose_name = u'文章'


class Tag(models.Model):
    name = models.CharField(u'标签名字', max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'标签'
        verbose_name = u'标签'


class Category(models.Model):
    DRAFT = 0
    PUBLISH = 1
    REMOVE = 2
    STATUS = {
        DRAFT: u'草稿',
        PUBLISH: u'正常',
        REMOVE: u'删除',
    }
    name = models.CharField(max_length=40, verbose_name=u'名称')
    status = models.IntegerField(choices=STATUS.items(), verbose_name=u'状态')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    def __str__(self):
        return "%s" % (self.name)

    @classmethod
    def available_list(cls):
        return cls.objects.filter(status=1)

    class Meta:
        verbose_name_plural = u'分类'
        verbose_name = u'分类'
