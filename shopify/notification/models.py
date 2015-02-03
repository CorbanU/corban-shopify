from __future__ import unicode_literals

import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from product.models import Product


logger = logging.getLogger(__name__)


class ProductNotification(models.Model):
    # Product for which notifications occur
    product = models.ForeignKey(Product)

    # Users to notify for this particular product
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return "Notification for %s" % self.product.description

    def notify_users(self, context):
        message = render_to_string('notification/product_notification.txt',
                                   context)
        recipients = [u.email for u in self.users.all()]
        try:
            send_mail('Corban Order Payment Received', message,
                      settings.DEFAULT_FROM_EMAIL, recipients)
        except SMTPException as e:
            logger.error("SMTP failed: %s" % e)
