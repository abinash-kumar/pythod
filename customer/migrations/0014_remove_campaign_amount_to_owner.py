# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-09-26 02:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0013_campaign_amount_to_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='amount_to_owner',
        ),
    ]
