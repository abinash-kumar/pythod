# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-08-10 19:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auraai', '0003_auto_20170809_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfbdetails',
            name='user_email',
            field=models.EmailField(blank=True, max_length=260),
        ),
    ]
