# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 22:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('willys_website', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homepage',
            options={'verbose_name': 'Homepage'},
        ),
        migrations.RenameField(
            model_name='homepage',
            old_name='body',
            new_name='intro_body',
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_intro',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='intro_title',
            field=models.TextField(blank=True),
        ),
    ]
