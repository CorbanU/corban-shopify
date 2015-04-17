from django.test import Client

from mock import patch
import pytest

from product.models import Product
from product.models import Transaction
from webhooks.models import Webhook


@pytest.mark.django_db
class TestRefunds:
    filename = 'fixtures/refunds-create.json'

    def test_refunds_create(self, json, hmac):
        Product.objects.create(product_id=123456, description='Sledgehammer')
        Product.objects.create(product_id=12345, description='Wire Cutter')
        with patch('requests.post') as mock:
            mock.return_value.status_code = 200
            mock.return_value.raise_for_status.return_value = None
            mock.return_value.raise_for_status()
            mock.return_value.json.return_value = {'webhook': {'id': 12345}}
            mock.return_value.json()
            hook = Webhook.objects.create(topic='refunds/create')

        c = Client()
        c.post(hook.path, data=json, content_type='text/json',
               HTTP_X_SHOPIFY_HMAC_SHA256=hmac)
        assert Transaction.objects.count() == 2
