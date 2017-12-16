# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-15 08:45
from __future__ import unicode_literals

from django.db import migrations
import utils.custom_image_field


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0035_auto_20171215_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=utils.custom_image_field.CustomImageField(blank=True, upload_to='thumbnail/user'),
        ),
    ]