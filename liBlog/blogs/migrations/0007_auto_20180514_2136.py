# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-14 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_auto_20180514_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish_time',
            field=models.DateTimeField(verbose_name='发布时间'),
        ),
    ]