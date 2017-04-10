# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-10 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('willys_website', '0010_standardpage_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardpage',
            name='form',
            field=models.CharField(choices=[('N', 'No Form'), ('Y', 'Form')], default=('N', 'No Form'), max_length=255),
        ),
    ]
