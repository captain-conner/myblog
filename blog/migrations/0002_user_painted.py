# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-13 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='painted',
            field=models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d', verbose_name='头像'),
        ),
    ]
