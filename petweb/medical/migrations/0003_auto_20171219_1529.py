# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 06:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0002_vaccineinoculation_num_of_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccineinoculation',
            name='hospital',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='vaccineinoculation',
            name='is_alarm',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='vaccineinoculation',
            name='inoculated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
