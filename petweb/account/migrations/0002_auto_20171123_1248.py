# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 03:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='활성화'),
        ),
    ]
