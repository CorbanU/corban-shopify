from __future__ import unicode_literals

import logging
import uuid

from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import requests

from .utils import shopify_api


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Webhook(models.Model):
    TOPIC_CHOICES = (
        ('orders/create', 'Order creation'),
        ('orders/delete', 'Order deletion'),
        ('orders/updated', 'Order update'),
        ('orders/paid', 'Order payment'),
        ('orders/cancelled', 'Order cancellation'),
        ('orders/fulfilled', 'Order fulfillment'),
        ('carts/create', 'Cart creation'),
        ('carts/update', 'Cart update'),
        ('checkouts/create', 'Checkout creation'),
        ('checkouts/update', 'Checkout update'),
        ('checkouts/delete', 'Checkout deletion'),
        ('refunds/create', 'Refund create'),
        ('products/create', 'Product creation'),
        ('products/update', 'Product update'),
        ('products/delete', 'Product deletion'),
        ('collections/create', 'Collection creation'),
        ('collections/update', 'Collection update'),
        ('collections/delete', 'Collection deletion'),
        ('customer_groups/create', 'Customer group creation'),
        ('customer_groups/update', 'Customer group update'),
        ('customer_groups/delete', 'Customer group deletion'),
        ('customers/create', 'Customer creation'),
        ('customers/enable', 'Customer enable'),
        ('customers/disable', 'Customer disable'),
        ('customers/update', 'Customer update'),
        ('customers/delete', 'Customer deletion'),
        ('fulfillments/create', 'Fulfillment creation'),
        ('fulfillments/update', 'Fulfillment update'),
        ('shop/update', 'Shop update'),
    )

    # Automatically generated GUID for the local webhook. This
    # GUID is also used to construct a unique URL.
    id = models.CharField(primary_key=True, default=uuid.uuid4,
                          max_length=36, editable=False)

    # An accepted event that will trigger the webhook
    topic = models.CharField(max_length=32, choices=TOPIC_CHOICES)

    # A unique Shopify ID for the webhook
    webhook_id = models.IntegerField(editable=False)

    def __str__(self):
        return self.path

    def save(self, *args, **kwargs):
        if not self.webhook_id:
            self.create()
        super(Webhook, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.webhook_id:
            self.remove()
        super(Webhook, self).delete(*args, **kwargs)

    @property
    def path(self):
        return "/%s/%s/" % (self.topic, self.id)

    def get_absolute_url(self):
        base = 'https://%s' % Site.objects.get_current().domain
        return base + self.path

    def create(self):
        payload = {'webhook': {'topic': self.topic,
                               'address': self.get_absolute_url(),
                               'format': 'json'}}
        try:
            resp = requests.post(shopify_api('/admin/webhooks.json'),
                                 json=payload)
            resp.raise_for_status()
            webhook_id = resp.json()['webhook']['id']
        except requests.exceptions.RequestException:
            logger.error("Webhook creation returned %s: %s" % (resp.status_code,
                                                               resp.text))
        else:
            self.webhook_id = webhook_id

    def remove(self):
        try:
            resp = requests.delete(shopify_api('/admin/webhooks/%d.json' % self.webhook_id))
            resp.raise_for_status()
        except requests.exceptions.RequestException:
            logger.error("Webhook removal returned %s: %s" % (resp.status_code,
                                                              resp.text))
