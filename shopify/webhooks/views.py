import json

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import View

from .models import Webhook
from .utils import verify_webhook
from notification.models import ProductNotification
from product.models import Product
from product.models import Transaction


class ValidateMixin(object):
    def post(self, request, *args, **kwargs):
        # Validate provided UUID
        uuid = self.kwargs.get('uuid')
        try:
            Webhook.objects.get(id=uuid)
        except Webhook.DoesNotExist:
            return HttpResponseBadRequest()

        # Validate received data
        hmac_sha256 = request.META.get('HTTP_X_SHOPIFY_HMAC_SHA256', None)
        if not verify_webhook(request.body, hmac_sha256):
            return HttpResponseBadRequest()

        super(ValidateMixin, self).post(request, *args, **kwargs)


class OrdersPaidView(ValidateMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        for item in data['line_items']:
            ProductNotification.objects.notify_users(item, data)
            Transaction.objects.add_transaction(item['product_id'],
                                                data['order_id'],
                                                data['order_number'],
                                                item['price'] * item['quantity'])
        return HttpResponse()


class ProductsCreateView(ValidateMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        Product.objects.create(product_id=data['id'], description=data['title'])
        return HttpResponse()


class ProductsUpdateView(ValidateMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        Product.objects.filter(product_id=data['id']).update(description=data['title'])
        return HttpResponse()
