import json

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import View

from webhook.utils import verify_webhook


class OrderPaymentView(View):
    def post(self, request, *args, **kwargs):
        # Validate received data
        hmac_sha256 = request.META.get('HTTP_X_SHOPIFY_HMAC_SHA256', None)
        if not verify_webhook(request.body, hmac_sha256):
            return HttpResponseBadRequest()

        data = json.loads(request.body)
        for item in data['line_items']:
            product_id = item['product_id']
            # TODO extract additional item data
            # TODO send notification based on product id
        return HttpResponse()
