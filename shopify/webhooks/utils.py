import base64
import hashlib
import hmac
from urlparse import urlunparse

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def calculate_hmac(data):
    """
    Generate a SHA256 HMAC from the given data and the
    configured shared secret.
    """
    shared_secret = getattr(settings, 'SHOPIFY_SHARED_SECRET', None)
    if shared_secret is None:
        err = ('SHOPIFY_SHARED_SECRET must be specified in your '
               'Django settings file')
        raise ImproperlyConfigured(err)

    digest = hmac.new(shared_secret, data, hashlib.sha256).digest()
    return base64.b64encode(digest)


def verify_webhook(data, hmac_header):
    """
    Verify that the given data matches the given HMAC header.
    """
    if not hmac_header:
        return False
    # TODO switch to hmac.compare_digest(a, b) once on Python 2.7.7
    return calculate_hmac(data) == hmac_header


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
