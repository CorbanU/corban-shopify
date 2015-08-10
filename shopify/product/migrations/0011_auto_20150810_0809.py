# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20150430_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='item_id',
            field=models.BigIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order_id',
            field=models.BigIntegerField(),
            preserve_default=True,
        ),
    ]
