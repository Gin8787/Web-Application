# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-06 00:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0004_auto_20171005_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='friends',
            field=models.ManyToManyField(related_name='followees', to=settings.AUTH_USER_MODEL),
        ),
    ]
