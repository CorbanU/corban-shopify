# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webhook',
            name='webhook_id',
            field=models.BigIntegerField(editable=False),
            preserve_default=True,
        ),
    ]
