import base64
import hashlib
import hmac
from urlparse import urlunparse

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def verify_webhook(data, hmac_header):
    if not hmac_header:
        return False

    shared_secret = getattr(settings, 'SHOPIFY_SHARED_SECRET', None)
    if shared_secret is None:
        err = ('SHOPIFY_SHARED_SECRET must be specified in your '
               'Django settings file')
        raise ImproperlyConfigured(err)

    digest = hmac.new(shared_secret, data, hashlib.sha256).digest()
    calculated_hmac = base64.b64encode(digest)
    return calculated_hmac == hmac_header


def shopify_api(path, query=''):
    """
    Generate a Shopify API URL in the format:
    https://apikey:password@hostname/admin/resource.json
    """
    api_key = getattr(settings, 'SHOPIFY_API_KEY', None)
    if api_key is None:
        err = ('SHOPIFY_API_KEY must be specified in your '
               'Django settings file')
        raise ImproperlyConfigured(err)

    password = getattr(settings, 'SHOPIFY_PASSWORD', None)
    if password is None:
        err = ('SHOPIFY_PASSWORD must be specified in your '
               'Django settings file')
        raise ImproperlyConfigured(err)

    hostname = getattr(settings, 'SHOPIFY_HOSTNAME', None)
    if hostname is None:
        err = ('SHOPIFY_HOSTNAME must be specified in your '
               'Django settings file')
        raise ImproperlyConfigured(err)

    netloc = '@'.join([':'.join([api_key, password]), hostname])
    return urlunparse(('https', netloc, path, '', query, ''))
