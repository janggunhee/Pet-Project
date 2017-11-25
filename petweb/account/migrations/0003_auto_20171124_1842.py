# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20171123_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='social_id',
            field=models.CharField(blank=True, max_length=255, unique=True, verbose_name='소셜 아이디'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, unique=True, verbose_name='이메일 주소'),
        ),
    ]
