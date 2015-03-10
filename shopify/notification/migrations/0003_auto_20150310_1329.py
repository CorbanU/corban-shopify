# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_productnotification_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productnotification',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productnotification',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
