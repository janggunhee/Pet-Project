# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 08:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetMedical',
            fields=[
                ('pet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='medical', serialize=False, to='account.Pet')),
            ],
        ),
        migrations.CreateModel(
            name='PetOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to=None)),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=50)),
                ('comment', models.TextField(blank=True, max_length=500)),
                ('pet_operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pet_operations', to='medical.PetMedical')),
            ],
        ),
        migrations.CreateModel(
            name='PetSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('chest', models.IntegerField(blank=True, null=True)),
                ('neck', models.IntegerField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='size', to='medical.PetMedical')),
            ],
        ),
        migrations.CreateModel(
            name='PetVaccine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn', models.PositiveIntegerField(blank=True, null=True)),
                ('date', models.DateField()),
                ('period', models.CharField(blank=True, max_length=30, null=True)),
                ('due_date', models.DateField()),
                ('hospital', models.CharField(blank=True, max_length=30)),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccines', to='medical.PetMedical')),
            ],
        ),
        migrations.CreateModel(
            name='VaccineInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine_name', models.CharField(blank=True, max_length=20)),
                ('vaccine_turn', models.PositiveIntegerField(default=0)),
                ('vaccine_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.PetSpecies')),
            ],
        ),
        migrations.AddField(
            model_name='petvaccine',
            name='vaccine_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.VaccineInfo'),
        ),
    ]
