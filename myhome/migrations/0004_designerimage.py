# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-05 06:24
from __future__ import unicode_literals

from django.db import migrations, models
import myhome.models


class Migration(migrations.Migration):

    dependencies = [
        ('myhome', '0003_categoryimage_otherbanners_sliderimages'),
    ]

    operations = [
        migrations.CreateModel(
            name='DesignerImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designer', models.CharField(max_length=150)),
                ('image_on_page', models.ImageField(blank=True, default=b'uploads/blogimages/dummy.jpg', null=True, upload_to=myhome.models.home_page_image_upload)),
            ],
        ),
    ]
