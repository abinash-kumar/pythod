# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-03-25 15:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20170129_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(max_length=60, null=True),
        ),
    ]