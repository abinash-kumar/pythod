# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-01-03 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20161204_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
