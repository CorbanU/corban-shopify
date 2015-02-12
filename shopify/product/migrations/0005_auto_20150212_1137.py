# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_product_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='price',
            new_name='amount',
        ),
        migrations.AddField(
            model_name='transaction',
            name='is_credit',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
