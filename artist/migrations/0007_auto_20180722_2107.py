# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-07-22 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0006_productartistdesignmap_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productartistdesignmap',
            name='product_type',
            field=models.CharField(choices=[(b'men-plain-tshirt', b'men-plain-tshirt'), (b'men-half-sleeves-round-neck-tshirt', b'men-half-sleeves-round-neck-tshirt'), (b'men-vest', b'men-vest'), (b'men-full-sleeves-round-neck-tshirt', b'men-full-sleeves-round-neck-tshirt'), (b'men-polo-tshirt', b'men-polo-tshirt'), (b'women-plain-tshirt', b'women-plain-tshirt'), (b'women-half-sleeves-round-neck-tshirt', b'women-half-sleeves-round-neck-tshirt'), (b'croptop', b'croptop'), (b'women-full-sleeves-round-neck-tshirt', b'women-full-sleeves-round-neck-tshirt'), (b'women-polo-tshirt', b'women-polo-tshirt')], max_length=150),
        ),
    ]
