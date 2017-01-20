import factory
from factory import fuzzy
from mock import patch

from django.utils.timezone import now

from shopify.product.models import Product
from shopify.product.models import Transaction
from shopify.webhook.models import Webhook


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_id = fuzzy.FuzzyInteger(100000, 999999)
    product_type = fuzzy.FuzzyChoice(['Deposit', 'Fee', 'Purchase'])
    description = fuzzy.FuzzyText(length=64)
    account_number = fuzzy.FuzzyInteger(1000000, 9999999)


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    product = factory.SubFactory(ProductFactory)
    amount = fuzzy.FuzzyFloat(1.00, 100.00)
    is_credit = True
    order_id = fuzzy.FuzzyInteger(1000000, 9999999)
    order_name = fuzzy.FuzzyText(length=8)
    item_id = fuzzy.FuzzyInteger(100000, 999999)
    created_at = now()


class WebhookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Webhook

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        with patch('requests.post') as mock:
            mock.return_value.status_code = 200
            mock.return_value.raise_for_status.return_value = None
            mock.return_value.raise_for_status()
            mock.return_value.json.return_value = {'webhook': {'id': 12345}}
            mock.return_value.json()
            return super(WebhookFactory, cls)._create(target_class, *args, **kwargs)
