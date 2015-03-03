# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20150212_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='order_number',
        ),
        migrations.AddField(
            model_name='transaction',
            name='order_name',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
    ]
