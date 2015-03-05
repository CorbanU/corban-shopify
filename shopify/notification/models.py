from __future__ import unicode_literals

import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.encoding import python_2_unicode_compatible

from product.models import Product


logger = logging.getLogger(__name__)


class ProductNotificationManager(models.Manager):
    def notify_users(self, item, data):
        product_id = item['product_id']
        try:
            notify = ProductNotification.objects.get(product__product_id=product_id)
        except ProductNotification.DoesNotExist:
            pass
        else:
            context = data
            # Duplicate the product data into the context dict so we
            # easily know the specific product we're notifying for
            context['product'] = item
            notify.send_notification(context)


@python_2_unicode_compatible
class ProductNotification(models.Model):
    # Product for which notifications occur
    product = models.ForeignKey(Product)

    # Users to notify for this particular product
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    objects = ProductNotificationManager()

    def __str__(self):
        return "%s notification" % self.product.description

    def get_recipients(self):
        return [user.email for user in self.users.all()]

    def send_notification(self, context):
        message = render_to_string('notification/product_notification.txt',
                                   context)
        try:
            send_mail('Corban Order Payment Received', message,
                      settings.DEFAULT_FROM_EMAIL, self.get_recipients())
        except SMTPException as e:
            logger.error("SMTP failed: %s" % e)
