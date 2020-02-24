# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-08-22 17:53
from __future__ import unicode_literals

import auraai.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_productartist'),
        ('auraai', '0004_auto_20170811_0048'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTagMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=150)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Category')),
            ],
        ),
        migrations.CreateModel(
            name='TagBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_name', models.CharField(max_length=50)),
                ('banner_image', models.ImageField(blank=True, default='uploads/blogimages/dummy.jpg', null=True, upload_to=auraai.models.f)),
                ('tags', models.ManyToManyField(to='auraai.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='producttagmap',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auraai.Tag'),
        ),
    ]