# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-08-06 18:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_remove_customer_is_designer'),
        ('product', '0018_cart_product_varient'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductArtist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commission', models.DecimalField(decimal_places=2, max_digits=15)),
                ('artist_words', models.CharField(max_length=200)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
            ],
        ),
    ]
