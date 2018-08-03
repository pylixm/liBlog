from django.db import models


# Create your models here.


class Book(models.Model):
    name = models.CharField('教程名字', max_length=100)
    image_url = models.CharField('教程封面', max_length=200, null=True, blank=True)
    author = models.CharField('作者', max_length=20)
    view_count = models.IntegerField('阅读量', default=0)
    summary = models.TextField('摘要', default=None, null=True, blank=True)
    book_url = models.CharField('教程url', max_length=100)

    def __str__(self):
        return '%s' % self.name
