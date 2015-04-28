import factory
from factory import fuzzy
from mock import patch

from product.models import Product
from webhooks.models import Webhook


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_id = fuzzy.FuzzyInteger(100000, 999999)
    product_type = fuzzy.FuzzyChoice(['Deposit', 'Fee', 'Purchase'])
    description = fuzzy.FuzzyText(length=64)
    account_number = fuzzy.FuzzyInteger(1000000, 9999999)


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
