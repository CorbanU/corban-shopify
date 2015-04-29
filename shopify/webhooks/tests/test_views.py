from django.test import Client

import pytest

from .factories import ProductFactory
from .factories import WebhookFactory
from product.models import Transaction


pytestmark = pytest.mark.django_db


class TestOrders:
    filename = 'orders-paid.json'

    def test_orders_paid(self, json, hmac):
        ProductFactory(product_id=123456)
        ProductFactory(product_id=12345)
        hook = WebhookFactory(topic='orders/paid')

        c = Client()
        c.post(hook.path, data=json, content_type='text/json',
               HTTP_X_SHOPIFY_HMAC_SHA256=hmac)
        assert Transaction.objects.count() == 2


class TestRefunds:
    filename = 'refunds-create.json'

    def test_refunds_create(self, json, hmac):
        ProductFactory(product_id=123456)
        ProductFactory(product_id=12345)
        hook = WebhookFactory(topic='refunds/create')

        c = Client()
        c.post(hook.path, data=json, content_type='text/json',
               HTTP_X_SHOPIFY_HMAC_SHA256=hmac)
        assert Transaction.objects.count() == 2
