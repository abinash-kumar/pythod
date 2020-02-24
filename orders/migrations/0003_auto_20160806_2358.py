# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-06 23:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20160806_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='shipping_charge',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payment_mode',
            field=models.CharField(choices=[('ONLINE', 'ONLINE'), ('COD', 'COD')], max_length=50),
        ),
    ]
