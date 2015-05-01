import json

from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from django.http import HttpResponse
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
            raise Http404

        # Validate received data
        hmac_sha256 = request.META.get('HTTP_X_SHOPIFY_HMAC_SHA256', None)
        if not verify_webhook(request.body, hmac_sha256):
            raise SuspiciousOperation('Invalid HMAC header provided')


class OrdersPaidView(ValidateMixin, View):
    def post(self, request, *args, **kwargs):
        super(OrdersPaidView, self).post(request, *args, **kwargs)
        data = json.loads(request.body)
        for item in data['line_items']:
            ProductNotification.objects.notify_users(item, data)
            Transaction.objects.add_transaction(item['product_id'],
                                                item['price'],
                                                item['quantity'],
                                                order_id=data['id'],
                                                order_name=data['name'],
                                                item_id=item['id'])
        return HttpResponse()


class ProductsCreateView(ValidateMixin, View):
    def post(self, request, *args, **kwargs):
        super(ProductsCreateView, self).post(request, *args, **kwargs)
        data = json.loads(request.body)
        Product.objects.create(product_id=data['id'],
                               product_type=data['product_type'],
                               description=data['title'])
        return HttpResponse()


class ProductsUpdateView(ValidateMixin, View):
    def post(self, request, *args, **kwargs):
        super(ProductsUpdateView, self).post(request, *args, **kwargs)
        data = json.loads(request.body)
        Product.objects.filter(product_id=data['id']).update(product_type=data['product_type'],
                                                             description=data['title'])
        return HttpResponse()


class RefundsCreateView(ValidateMixin, View):
    def post(self, request, *args, **kwargs):
        super(RefundsCreateView, self).post(request, *args, **kwargs)
        data = json.loads(request.body)
        for refund in data['refund_line_items']:
            item = refund['line_item']
            Transaction.objects.add_transaction(item['product_id'],
                                                item['price'],
                                                item['quantity'],
                                                credit=False,
                                                order_id=data['order_id'],
                                                item_id=item['id'])
        return HttpResponse()
