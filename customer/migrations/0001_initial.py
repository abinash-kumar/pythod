# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-01-28 06:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myhome', '0007_auto_20170128_0324')
    ]

    state_operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=60)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'male'), ('FEMALE', 'female')], max_length=60, null=True)),
                ('is_mobile_verified', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ab_customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('pin_code', models.IntegerField(null=True)),
                ('city', models.CharField(blank=True, max_length=60, null=True)),
                ('state', models.CharField(blank=True, max_length=60, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ab_customer', to='customer.Customer')),
            ],
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
