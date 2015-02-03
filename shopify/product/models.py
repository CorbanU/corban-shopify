from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Product(models.Model):
    # Shopify product ID number for unique identification
    product_id = models.IntegerField()

    # Informative description, only used for display purposes
    description = models.CharField(max_length=255)

    # Internal account number for this product
    account_number = models.IntegerField()

    def __str__(self):
        return self.description
