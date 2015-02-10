# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20150206_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='order_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='order_number',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
