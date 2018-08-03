import datetime
import sys
import traceback
import logging

from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.views.generic import ListView, View
from django.views.generic.base import ContextMixin

from config import settings
from .models import Book

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
            context['site_publish_days'] = (
                        datetime.datetime.now() - publish_time).days
            context['last_publish_days'] = (
                        datetime.datetime.now() - last_publish_time).days
        except Exception as e:
            logger.error(" ".join(traceback.format_exception(*sys.exc_info())))
        return context


class IndexView(BaseMixin, ListView):
    queryset = Book.objects.all()
    template_name = 'tutorial/index.html'
    # 指定 queryset 的名字
    context_object_name = 'book_list'


class CountView(View):

    def post(self, request):
        book_id = request.POST.get('id')
        ret = {
            'status': 0
        }
        if book_id:
            book = Book.objects.get(id=book_id)
            book.view_count += 1
            book.save()
            ret.update({
                'status': 1
            })
        return JsonResponse(ret)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(CountView, self).dispatch(*args, **kwargs)
