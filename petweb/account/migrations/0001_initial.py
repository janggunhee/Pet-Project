# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 08:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone
import utils.django.custom_image_field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_type', models.CharField(choices=[('f', 'facebook'), ('g', 'google'), ('d', 'django')], default='d', max_length=1)),
                ('image', utils.django.custom_image_field.CustomImageField(blank=True, max_length=255, upload_to='thumbnail/user')),
                ('email', models.EmailField(blank=True, max_length=255, unique=True, verbose_name='email_address')),
                ('social_id', models.CharField(blank=True, max_length=255, verbose_name='social_id')),
                ('nickname', models.CharField(max_length=255, unique=True, verbose_name='nickname')),
                ('is_active', models.BooleanField(default=False, verbose_name='is_active')),
                ('device_token', models.CharField(blank=True, max_length=160, verbose_name='device_token')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date_joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ('-date_joined',),
            },
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', utils.django.custom_image_field.CustomImageField(blank=True, upload_to='thumbnail/pet')),
                ('name', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('male', '수컷'), ('female', '암컷')], max_length=10)),
                ('identified_number', models.CharField(blank=True, max_length=20)),
                ('is_neutering', models.BooleanField(default=False)),
                ('body_color', models.CharField(choices=[('black', '검정색'), ('white', '하얀색'), ('brown', '갈색'), ('gold', '황금색')], max_length=10)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-pk',),
            },
        ),
        migrations.CreateModel(
            name='PetBreed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breeds_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PetSpecies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_type', models.CharField(choices=[('dog', '강아지'), ('cat', '고양이')], max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Pet species',
            },
        ),
        migrations.AddField(
            model_name='petbreed',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.PetSpecies'),
        ),
        migrations.AddField(
            model_name='pet',
            name='breeds',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.PetBreed'),
        ),
        migrations.AddField(
            model_name='pet',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pet',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.PetSpecies'),
        ),
    ]
