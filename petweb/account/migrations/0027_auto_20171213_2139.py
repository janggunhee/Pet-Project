# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 12:39
from __future__ import unicode_literals

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_auto_20171213_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, default='placeholder/placeholder_human.png', null=True, upload_to='Users', verbose_name='thumbnail'),
        ),
    ]