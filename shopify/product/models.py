from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now


@python_2_unicode_compatible
class Product(models.Model):
    # Shopify product ID number for unique identification
    product_id = models.IntegerField(unique=True)

    # Informative description, only used for display purposes
    description = models.CharField(max_length=255)

    # Internal account number for this product
    account_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.description


class TransactionManager(models.Manager):
    def add_transaction(self, id, price):
        try:
            product = Product.objects.get(product_id=id)
        except Product.DoesNotExist:
            pass
        else:
            self.create(product=product, price=price, created_at=now())


class Transaction(models.Model):
    # Product for which this transaction occurred
    product = models.ForeignKey(Product)

    # Price of product for this transaction
    price = models.DecimalField(decimal_places=2, max_digits=6)

    # When the transaction occurred
    created_at = models.DateTimeField()

    # Set when a transaction has been exported
    exported_at = models.DateTimeField(editable=False, null=True)

    objects = TransactionManager()
