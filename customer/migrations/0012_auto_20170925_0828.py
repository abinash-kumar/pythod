# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-09-25 02:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_auto_20170923_1621'),
    ]

    operations = [
        migrations.RenameField(
            model_name='abmoney',
            old_name='closing_cash_money',
            new_name='_closing_cash_money',
        ),
        migrations.RenameField(
            model_name='abmoney',
            old_name='closing_promotional_money',
            new_name='_closing_promotional_money',
        ),
        migrations.AddField(
            model_name='campaign',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 9, 25, 8, 28, 57, 920354)),
            preserve_default=False,
        ),
    ]
