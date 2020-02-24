# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-07-31 20:37
from __future__ import unicode_literals

from django.db import migrations

def create_tshirt_categories(app, schema_editor):
    from product.models import Category, CategoryVarient
    
    category = Category.objects.get(id=381)
    CategoryVarient.objects.create(category=category, varient_type="FABRIC", value="COTTON")
    CategoryVarient.objects.create(category=category, varient_type="FITTING", value="REGULAR")
    CategoryVarient.objects.create(category=category, varient_type="FITTING", value="LOOSE")
    CategoryVarient.objects.create(category=category, varient_type="FITTING", value="SLIM")
    CategoryVarient.objects.create(category=category, varient_type="NECK", value="POLO")
    CategoryVarient.objects.create(category=category, varient_type="NECK", value="COWL NECK")
    CategoryVarient.objects.create(category=category, varient_type="NECK", value="ROUND NECK")
    CategoryVarient.objects.create(category=category, varient_type="NECK", value="V NECK")
    CategoryVarient.objects.create(category=category, varient_type="SLEEVES", value="3/4 SLEEVE")
    CategoryVarient.objects.create(category=category, varient_type="SLEEVES", value="HALF SLEEVE")
    CategoryVarient.objects.create(category=category, varient_type="SLEEVES", value="FULL SLEEVE")









class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_auto_20170729_2121'),
    ]

    operations = [
        migrations.RunPython(create_tshirt_categories)
    ]