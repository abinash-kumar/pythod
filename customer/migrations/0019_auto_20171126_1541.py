# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-11-26 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0018_coupon_redeem_amount_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abmoney',
            name='amount_type',
            field=models.CharField(choices=[('PROMOTIONAL', 'PROMOTIONAL'), ('CASH', 'CASH'), ('TRANSACTIONAL', 'TRANSACTIONAL')], max_length=60),
        ),
    ]
