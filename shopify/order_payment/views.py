import json

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import View

from .models import ProductNotification
from .utils import verify_webhook


class OrderPaymentView(View):
    def post(self, request, *args, **kwargs):
        # Validate received data
        hmac_sha256 = request.META.get('HTTP_X_SHOPIFY_HMAC_SHA256', None)
        if not verify_webhook(request.body, hmac_sha256):
            return HttpResponseBadRequest()

        data = json.loads(request.body)
        for item in data['line_items']:
            try:
                product_notify = ProductNotification.objects.get(product_id=item['product_id'])
            except ProductNotification.DoesNotExist:
                pass
            else:
                context = data
                # Duplicate the product data into the context dict so we
                # easily know the specific product we're notifying for
                context['product'] = item
                product_notify.notify_users(context)
        return HttpResponse()
