from __future__ import unicode_literals

from decimal import Decimal
import logging

from django.db import IntegrityError
from django.db import models
from django.db.models import Sum
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Product(models.Model):
    # Unique Shopify product ID number
    product_id = models.BigIntegerField(unique=True)

    # Type for this product (fee, deposit, etc.)
    product_type = models.CharField(max_length=64, blank=True)

    # Informative description, used for display purposes
    description = models.CharField(max_length=255)

    # Internal account number for this product
    account_number = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.description


class TransactionManager(models.Manager):
    def add_transaction(self, product_id, price, quantity, credit=True, **kwargs):
        if not product_id:
            return
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            logger.warning("Could not add transaction for non-existent product %d" % product_id)
        else:
            amount = Decimal(price) * Decimal(quantity)
            try:
                self.create(product=product, amount=amount, is_credit=credit,
                            created_at=now(), **kwargs)
            except IntegrityError as e:
                order_name = kwargs.pop('order_name', '')
                logger.warning("Error adding transaction %s: %s" % (order_name, e))

    def get_amounts(self):
        """
        Return aggregated transaction amounts of all transactions
        that have not already been exported and have a product
        account number. All returned transactions are marked as
        exported.
        """
        transactions = self.filter(exported_at__isnull=True).exclude(product__account_number__isnull=True)
        # Force queryset evaluation so we can call update on the queryset
        amounts = list(transactions.values('product__account_number', 'order_name', 'is_credit').order_by('created_at').annotate(amount=Sum('amount')))
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
    order_id = models.BigIntegerField()

    # Shopify order name for the transaction; not available
    # if this is a refund
    order_name = models.CharField(max_length=16, blank=True)

    # Shopify item ID for the transaction
    item_id = models.BigIntegerField()

    # When the transaction occurred
    created_at = models.DateTimeField(editable=False)

    # When the transaction was exported
    exported_at = models.DateTimeField(editable=False, null=True)

    objects = TransactionManager()

    class Meta:
        unique_together = ('is_credit', 'order_id', 'item_id')
