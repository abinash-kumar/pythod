# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-08-04 22:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_auto_20170801_0207'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='product_varient',
            field=models.ForeignKey(default=921, on_delete=django.db.models.deletion.CASCADE, to='product.ProductVarientList'),
            preserve_default=False,
        ),
    ]
