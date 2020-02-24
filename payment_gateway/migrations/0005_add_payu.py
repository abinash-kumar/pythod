# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations


def add_record(apps, schema_editor):
    payment_gateway = apps.get_model('payment_gateway', 'PaymentGateway')
    payment_gateway.objects.create(
        slug='payu',
        title='PayU India',
        body='Simplified payment solutions. Build to deliver an awesome customer experience',
        is_active=True
    )


class Migration(migrations.Migration):
    dependencies = [
        ('payment_gateway', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=add_record,
            reverse_code=migrations.RunPython.noop,
        )
    ]
