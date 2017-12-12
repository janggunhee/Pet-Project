# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 11:31
from __future__ import unicode_literals

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20171212_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(height_field='height', upload_to='%(class)', width_field='width'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(height_field='height', upload_to='%(class)', width_field='width'),
        ),
    ]
