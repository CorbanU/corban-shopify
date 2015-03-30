# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20150302_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='item_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
