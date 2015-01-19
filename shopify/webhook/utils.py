import base64
import hashlib
import hmac

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def verify_webhook(data, hmac_header):
    shared_secret = getattr(settings, 'SHOPIFY_SHARED_SECRET', None)
    if shared_secret is None:
        err = ('SHOPIFY_SHARED_SECRET must be specified in your '
               'Django settings file')
        raise ImproperlyConfigured(err)

    digest = hmac.new(shared_secret, data, hashlib.sha256).digest()
    calculated_hmac = base64.b64encode(digest)
    return calculated_hmac == hmac_header
