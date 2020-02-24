# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-09-15 22:31
from __future__ import unicode_literals

from django.db import migrations

def forward(apps, schema_editor):
    #product_varient_list = apps.get_model("ProductVarientList")
    from orders.models import Order
    from product.models import ProductVarientList
    for order in Order.objects.all():
        product = order.product_id
        pvl = ProductVarientList.objects.filter(product=product)
        if len(pvl) > 0:
            order.product_varient = pvl[0]
            order.save()


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20170916_0359'),
    ]

    operations = [
        migrations.RunPython(forward)
    ]
