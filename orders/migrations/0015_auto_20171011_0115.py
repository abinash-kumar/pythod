# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-10-10 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20170925_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_request',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payment_response',
            field=models.TextField(default=None, null=True),
        ),
    ]
