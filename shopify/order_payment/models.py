from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class ProductNotification(models.Model):
    product_id = models.IntegerField()
    description = models.CharField(max_length=255)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.description
