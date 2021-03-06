# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-31 12:28
from __future__ import unicode_literals

from django.db import migrations, models
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20160724_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_photo',
            field=models.ImageField(blank=True, default='uploads/blogimages/dummy.jpg', null=True, upload_to=product.models.category_image_upload),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='product.Category'),
        ),
    ]
