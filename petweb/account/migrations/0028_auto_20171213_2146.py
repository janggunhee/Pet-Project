# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 12:46
from __future__ import unicode_literals

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_auto_20171213_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, default='placeholder/placeholder_pet.png', null=True, upload_to='Pets', verbose_name='thumbnail'),
        ),
    ]