# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-22 08:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='battle_tag',
            field=models.CharField(blank=True, default=' ', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_captain',
            field=models.BooleanField(default=False, help_text='Является ли капитаном команды', verbose_name='Капитан'),
        ),
        migrations.AddField(
            model_name='user',
            name='lol_name',
            field=models.CharField(blank=True, default=' ', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='steam_name',
            field=models.CharField(blank=True, default=' ', max_length=50, null=True),
        ),
    ]
