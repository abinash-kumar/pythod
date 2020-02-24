# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-24 09:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=60)),
                ('gender', models.CharField(blank=True, choices=[(b'MALE', b'male'), (b'FEMALE', b'female')], max_length=60, null=True)),
                ('shop_address', models.CharField(blank=True, max_length=200, null=True)),
                ('shop_pin_code', models.IntegerField(null=True)),
                ('shop_city', models.CharField(blank=True, max_length=60, null=True)),
                ('shop_state', models.CharField(blank=True, max_length=60, null=True)),
                ('pickup_address', models.CharField(blank=True, max_length=200, null=True)),
                ('pickup_pin_code', models.IntegerField(null=True)),
                ('pickup_city', models.CharField(blank=True, max_length=60, null=True)),
                ('pickup_state', models.CharField(blank=True, max_length=60, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SellerBankDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_holder_name', models.CharField(max_length=60)),
                ('bank_name', models.CharField(max_length=100)),
                ('branch_name', models.CharField(max_length=100)),
                ('pan', models.CharField(max_length=15)),
                ('ifsc_code', models.CharField(max_length=15)),
                ('account_no', models.CharField(max_length=30)),
                ('bank_branch_address', models.CharField(max_length=200)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Seller')),
            ],
        ),
        migrations.CreateModel(
            name='SellerOnboardingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timespam', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[(b'REGISTERED', b'Registered'), (b'PENDING_APPROVAL', b'pending_approval'), (b'APPROVED', b'approved')], default=((b'REGISTERED', b'Registered'), (b'PENDING_APPROVAL', b'pending_approval'), (b'APPROVED', b'approved')), max_length=20)),
                ('active_status', models.BooleanField(default=False)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Seller')),
            ],
        ),
        migrations.CreateModel(
            name='SellerVatDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_tin', models.BooleanField(default=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('tin_no', models.CharField(blank=True, max_length=30, null=True)),
                ('cst_no', models.CharField(blank=True, max_length=30, null=True)),
                ('legal_address', models.CharField(blank=True, max_length=200, null=True)),
                ('legal_pin_code', models.IntegerField(null=True)),
                ('legal_city', models.CharField(blank=True, max_length=60, null=True)),
                ('legal_state', models.CharField(blank=True, max_length=60, null=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Seller')),
            ],
        ),
    ]
