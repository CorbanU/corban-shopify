from __future__ import unicode_literals

import uuid

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class Webhook(models.Model):
    ORDER_PAYMENT = 'order_payment'
    TYPE_CHOICES = (
        (ORDER_PAYMENT, 'Order Payment'),
    )

    id = models.CharField(primary_key=True, default=uuid.uuid4,
                          max_length=36, editable=False)
    hook_type = models.CharField(max_length=32, choices=TYPE_CHOICES)

    def __str__(self):
        return self.path

    @property
    def path(self):
        return "/%s/%s/" % (self.hook_type, self.id)
