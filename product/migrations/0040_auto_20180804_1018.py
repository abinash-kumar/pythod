# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-08-04 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0039_auto_20180730_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productoffer',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='productoffer',
            name='offer',
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='rule',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]