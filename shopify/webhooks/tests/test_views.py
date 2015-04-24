from django.test import Client

import pytest

from .factories import WebhookFactory
from product.models import Product
from product.models import Transaction


@pytest.mark.django_db
class TestOrders:
    filename = 'fixtures/orders-paid.json'

    def test_orders_paid(self, json, hmac):
        Product.objects.create(product_id=123456, description='Sledgehammer')
        Product.objects.create(product_id=12345, description='Wire Cutter')
        hook = WebhookFactory(topic='orders/paid')

        c = Client()
        c.post(hook.path, data=json, content_type='text/json',
               HTTP_X_SHOPIFY_HMAC_SHA256=hmac)
        assert Transaction.objects.count() == 2


@pytest.mark.django_db
class TestRefunds:
    filename = 'fixtures/refunds-create.json'

    def test_refunds_create(self, json, hmac):
        Product.objects.create(product_id=123456, description='Sledgehammer')
        Product.objects.create(product_id=12345, description='Wire Cutter')
        hook = WebhookFactory(topic='refunds/create')

        c = Client()
        c.post(hook.path, data=json, content_type='text/json',
               HTTP_X_SHOPIFY_HMAC_SHA256=hmac)
        assert Transaction.objects.count() == 2
