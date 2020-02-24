# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-01-05 01:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_cart_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='keywords',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_description',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='page_title',
            field=models.CharField(blank=True, default='Addiction Bazaar', max_length=200),
        ),
    ]