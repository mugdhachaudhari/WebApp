# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-21 03:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imageUploader', '0006_imagemodel_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemodel',
            name='user',
        ),
    ]
