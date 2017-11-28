# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 08:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20171128_1651'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='petspecies',
            options={},
        ),
        migrations.AddField(
            model_name='pet',
            name='species',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='account.PetSpecies'),
        ),
    ]