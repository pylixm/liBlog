# -*- coding:utf-8 -*-
import datetime

from django.conf import settings
from django.db.models import Count
from django import template

from liBlog.blogs.models import Tag

register = template.Library()


@register.filter
def conver_date(value):
    if not isinstance(value, datetime.datetime):
        return value
    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    interval_datetime = current_datetime - value
    if hasattr(interval_datetime, 'year'):
        return '%s年前' % interval_datetime.year
    elif hasattr(interval_datetime, 'month'):
        return '%s个月前' % interval_datetime.month
    elif hasattr(interval_datetime, 'days') and interval_datetime.days > 7:
        return '%s周前' % (interval_datetime.days / 7)
    elif hasattr(interval_datetime, 'days') and interval_datetime.days > 0:
        return '%s天前' % interval_datetime.days
    else:
        return value.strftime('%Y-%m-%d %H:%M:%S')


@register.simple_tag(takes_context=True)
def fill_ctx(context):
    # # 整站信息
    if 'site_ext' not in context:
        context['site_ext'] = settings.SITE
    # 标签
    if 'sidbar_tag_list' not in context:
        context['sidbar_tag_list'] = Tag.objects.values('name').annotate(
            post_count=Count('post_list')).filter(
            post_count__gt=settings.TAG_SIDE_SHOW_NUM).order_by('-post_count')
    # 发布时间
    publish_time = datetime.datetime.strptime(
        settings.SITE.get('publish_time', '2018-05-14 16:00:00'),
        '%Y-%m-%d %H:%M:%S')
    last_publish_time = datetime.datetime.strptime(
        settings.SITE.get('last_publish_time', '2018-05-14 16:00:00'),
        '%Y-%m-%d %H:%M:%S')
    context['site_publish_days'] = (datetime.datetime.now() - publish_time).days
    context['last_publish_days'] = (datetime.datetime.now() - last_publish_time).days
    return ''


if __name__ == '__main__':
    date = datetime.datetime.now() - datetime.timedelta(days=10)
    print(conver_date(date))
