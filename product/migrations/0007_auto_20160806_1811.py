# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-06 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20160804_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='cart',
            name='varient',
            field=models.CharField(default='NA', max_length=150),
        ),
    ]
