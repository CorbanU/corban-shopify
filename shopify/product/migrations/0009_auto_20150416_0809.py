# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20150331_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='order_name',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
    ]
