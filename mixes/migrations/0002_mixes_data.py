# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-07 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mixes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mixes',
            name='data',
            field=models.DateField(default='2000-01-01'),
        ),
    ]