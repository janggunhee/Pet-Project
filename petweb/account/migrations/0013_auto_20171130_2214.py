# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 13:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20171130_2213'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='petspecies',
            options={'verbose_name_plural': 'Pet species'},
        ),
    ]