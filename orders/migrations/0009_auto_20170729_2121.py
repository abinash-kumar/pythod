# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-07-29 15:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20170325_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('DRAFT', 'DRAFT'), ('PENDING', 'PENDING'), ('CONFIRMED', 'CONFIRMED'), ('PAYMENT_DONE', 'PAYMENT_DONE'), ('COD', 'COD'), ('SHIPPED', 'SHIPPED'), ('DELIVERED', 'DELIVERED'), ('RETURNED', 'RETURNED'), ('CANCELLED', 'CANCELLED')], max_length=50),
        ),
    ]
