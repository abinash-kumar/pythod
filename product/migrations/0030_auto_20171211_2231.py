# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-12-11 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='category_varient',
            field=models.ManyToManyField(blank=True, to='product.CategoryVarient'),
        ),
    ]