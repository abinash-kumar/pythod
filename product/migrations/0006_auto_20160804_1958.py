# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-04 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20160804_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
    ]