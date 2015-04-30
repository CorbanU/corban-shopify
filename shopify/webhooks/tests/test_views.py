from django.test import Client

import pytest

from .factories import ProductFactory
from .factories import WebhookFactory
from product.models import Product
from product.models import Transaction


pytestmark = pytest.mark.django_db


class TestOrdersPaid:
    filename = 'orders-paid.json'

    def test_orders_paid(self, json, hmac):
        ProductFactory(product_id=123456)
        ProductFactory(product_id=12345)
        hook = WebhookFactory(topic='orders/paid')

        c = Client()
        c.post(hook.path, data=json, content_type='text/json',
               HTTP_X_SHOPIFY_HMAC_SHA256=hmac)
        assert Transaction.objects.count() == 2


class TestProductsCreate:
    filename = 'products-create.json'

    def test_products_create(self, json, hmac):
        hook = WebhookFactory(topic='products/create')

        c = Client()
        c.post(hook.path, data=json, content_type='text/json',
               HTTP_X_SHOPIFY_HMAC_SHA256=hmac)
        assert Product.objects.count() == 1


class TestProductsUpdate:
    filename = 'products-update.json'

    def test_products_update(self, json, hmac):
        ProductFactory(product_id=327475578523353102, product_type='Pants',
                       description='Example Pants')
        hook = WebhookFactory(topic='products/update')

        c = Client()
        c.post(hook.path, data=json, content_type='text/json',
               HTTP_X_SHOPIFY_HMAC_SHA256=hmac)
        product = Product.objects.get(product_id=327475578523353102)
        assert product.product_type == 'Shirts'
        assert product.description == 'Example T-Shirt'


class TestRefundsCreate:
    filename = 'refunds-create.json'

    def test_refunds_create(self, json, hmac):
        ProductFactory(product_id=123456)
        ProductFactory(product_id=12345)
        hook = WebhookFactory(topic='refunds/create')

        c = Client()
        c.post(hook.path, data=json, content_type='text/json',
               HTTP_X_SHOPIFY_HMAC_SHA256=hmac)
        assert Transaction.objects.count() == 2
