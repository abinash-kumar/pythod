# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-11-19 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_auto_20171102_0250'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='category_varient',
            field=models.ManyToManyField(to='product.CategoryVarient'),
        ),
    ]
