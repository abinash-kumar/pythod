# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-04-15 20:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_auto_20170401_0335'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerEmailVerify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', django_extensions.db.fields.UUIDField(blank=True, editable=False, unique=True)),
                ('is_clicked', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ab_customer_email_verify', to='customer.Customer')),
            ],
        ),
    ]
