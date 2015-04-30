# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20150416_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(editable=False),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together=set([('is_credit', 'order_id', 'item_id')]),
        ),
    ]
