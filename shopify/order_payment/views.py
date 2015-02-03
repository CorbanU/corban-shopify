import json

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import View

from .utils import verify_webhook
from notification.models import ProductNotification


class OrderPaymentView(View):
    def post(self, request, *args, **kwargs):
        # Validate received data
        hmac_sha256 = request.META.get('HTTP_X_SHOPIFY_HMAC_SHA256', None)
        if not verify_webhook(request.body, hmac_sha256):
            return HttpResponseBadRequest()

        data = json.loads(request.body)
        for item in data['line_items']:
            ProductNotification.objects.notify_users(item, data)
        return HttpResponse()
