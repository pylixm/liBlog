import datetime
import sys
import traceback
import logging

from django.db.models import Count
from django.views.generic import ListView

from config import settings

logger = logging.getLogger('')


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
        except Exception as e:
            logger.error(" ".join(traceback.format_exception(*sys.exc_info())))
        return context


class IndexView(BaseMixin, ListView):
    queryset = []
    template_name = 'tutorial/index.html'
    # 指定 queryset 的名字
    context_object_name = 'post_list'