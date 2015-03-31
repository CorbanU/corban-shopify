# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_transaction_item_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='item_id',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order_id',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order_name',
            field=models.CharField(max_length=16),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together=set([('order_id', 'item_id')]),
        ),
    ]
