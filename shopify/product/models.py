from __future__ import unicode_literals

from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now


@python_2_unicode_compatible
class Product(models.Model):
    # Shopify product ID number for unique identification
    product_id = models.IntegerField(unique=True)

    # Product type for which this transaction occurred
    product_type = models.CharField(max_length=64, blank=True)

    # Informative description, only used for display purposes
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

    def get_credits(self):
        credits = self.filter(exported_at__isnull=True, is_credit=True).exclude(product__account_number__isnull=True)
        # Force queryset evaluation so we can call update on the queryset
        result = list(credits.values('product__account_number', 'order_number').order_by('order_number').annotate(amount=Sum('amount')))
        credits.update(exported_at=now())
        return result

    def get_debits(self):
        debits = self.filter(exported_at__isnull=True, is_credit=False).exclude(product__account_number__isnull=True)
        # Force queryset evaluation so we can call update on the queryset
        result = list(debits.values('product__account_number', 'order_number').order_by('order_number').annotate(amount=Sum('amount')))
        debits.update(exported_at=now())
        return result


class Transaction(models.Model):
    # Product for which this transaction occurred
    product = models.ForeignKey(Product)

    # Amount (price * quantity) for this transaction
    amount = models.DecimalField(decimal_places=2, max_digits=6)

    # Specify if transaction type is credit or debit
    is_credit = models.BooleanField(default=True)

    # Shopify order id containing the transaction
    order_id = models.IntegerField(null=True, blank=True)

    # Order number containing the transaction
    order_number = models.IntegerField(null=True, blank=True)

    # When the transaction occurred
    created_at = models.DateTimeField()

    # Set when a transaction has been exported
    exported_at = models.DateTimeField(editable=False, null=True)

    objects = TransactionManager()
