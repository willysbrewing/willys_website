# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 08:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('willys_website', '0005_auto_20161220_0925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepagehero',
            name='title',
        ),
    ]
