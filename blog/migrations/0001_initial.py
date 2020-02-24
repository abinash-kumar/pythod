# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-02 20:26
from __future__ import unicode_literals

import blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(blank=True, editable=False, max_length=250)),
                ('title', models.CharField(max_length=250)),
                ('meta_description', models.CharField(blank=True, max_length=250, null=True)),
                ('image', models.ImageField(blank=True, default='uploads/blogimages/dummy.jpg', null=True, upload_to=blog.models.f)),
                ('image_text', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.CharField(max_length=5000)),
                ('posted_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('views', models.IntegerField(blank=True, null=True)),
                ('active', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50)),
                ('for_blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
            ],
        ),
    ]