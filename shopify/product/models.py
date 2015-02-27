from __future__ import unicode_literals

from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now


@python_2_unicode_compatible
class Product(models.Model):
    # Unique Shopify product ID number
    product_id = models.IntegerField(unique=True)

    # Type for this product (fee, deposit, etc.)
    product_type = models.CharField(max_length=64, blank=True)

    # Informative description, used for display purposes
    description = models.CharField(max_length=255)

    # Internal account number for this product
    account_number = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.description


class TransactionManager(models.Manager):
    def add_transaction(self, product_id, price, quantity,
                        credit=True, order_id=None, order_number=None):
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            pass
        else:
            amount = Decimal(price) * Decimal(quantity)
            self.create(product=product, amount=amount, is_credit=credit,
                        order_id=order_id, order_number=order_number,
                        created_at=now())

    def get_amounts(self, credit=True):
        """
        Return aggregated transaction amounts of all transactions
        that have not already been exported and have a product
        account number. All returned transactions are marked as
        exported.
        """
        transactions = self.filter(exported_at__isnull=True, is_credit=credit).exclude(product__account_number__isnull=True)
        # Force queryset evaluation so we can call update on the queryset
        amounts = list(transactions.values('product__account_number', 'order_number').order_by('order_number').annotate(amount=Sum('amount')))
        transactions.update(exported_at=now())
        return amounts


class Transaction(models.Model):
    # Product for which this transaction occurred
    product = models.ForeignKey(Product)

    # Amount (price * quantity) for this transaction
    amount = models.DecimalField(decimal_places=2, max_digits=6)

    # Specify if transaction type is credit or debit
    is_credit = models.BooleanField(default=True)

    # Shopify order ID for the transaction
    order_id = models.IntegerField(null=True, blank=True)

    # Order number for the transaction
    order_number = models.IntegerField(null=True, blank=True)

    # When the transaction occurred
    created_at = models.DateTimeField()

    # When the transaction was exported
    exported_at = models.DateTimeField(editable=False, null=True)

    objects = TransactionManager()
