# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-09-15 20:08
from __future__ import unicode_literals

from django.db import migrations

def forward(apps, schema_editor):
    #product_varient_list = apps.get_model("ProductVarientList")
    from product.models import ProductVarientList
    for pv in ProductVarientList.objects.all():
        seller = pv.product.seller
        pv.sellers.add(seller)


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_auto_20170916_0137'),
    ]

    operations = [
        migrations.RunPython(forward)
    ]
