# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-21 03:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imageUploader', '0004_auto_20160921_0311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemodel',
            name='user',
        ),
    ]
