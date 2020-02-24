# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-09-23 05:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0004_artistdetail_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artistdetail',
            name='artist_type',
            field=models.CharField(blank=True, choices=[('INDEPENDENT', 'INDEPENDENT'), ('YOUTUBER', 'YOUTUBER'), ('BLOGGER', 'BLOGGER'), ('NGO', 'NGO'), ('OTHER', 'OTHER')], max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='sociallink',
            name='website',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
