from __future__ import unicode_literals

import logging
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.encoding import python_2_unicode_compatible

import dateutil.parser

from shopify.product.models import Product


logger = logging.getLogger(__name__)


class ProductNotificationManager(models.Manager):
    def notify_users(self, item, data):
        product_id = item['product_id']
        if not product_id:
            return
        try:
            notify = ProductNotification.objects.get(product__product_id=product_id)
        except ProductNotification.DoesNotExist:
            logger.warning("No notifications configured for product %d" % product_id)
        else:
            context = data.copy()
            # Convert to a datetime object so we can format it
            # within the template
            context['created_at'] = dateutil.parser.parse(context['created_at'])
            # Duplicate the product data into the context dict so we
            # easily know the specific product we're notifying for
            context['product'] = item
            notify.send_notification(context)


@python_2_unicode_compatible
class ProductNotification(models.Model):
    # Product for which notifications occur
    product = models.ForeignKey(Product)

    # Users to notify for this product
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    # Groups of users to notify for this product
    groups = models.ManyToManyField(Group, blank=True)

    objects = ProductNotificationManager()

    def __str__(self):
        return "%s notification" % self.product.description

    def get_recipients(self):
        """
        Return a list of unique recipients from the associated
        users and groups.
        """
        recipients = set([user.email for user in self.users.all()])
        for group in self.groups.all():
            recipients.update([user.email for user in group.user_set.all()])
        return list(recipients)

    def send_notification(self, context):
        """
        Send an email notification to the designated recipients
        with the given context.
        """
        subject = "Order placed for %s [%s]" % (context['product']['name'], context['name'])
        message = render_to_string('notification/product_notification.txt',
                                   context)
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                      self.get_recipients())
        except SMTPException as e:
            logger.error("Error sending notification: %s" % e)
        else:
            logger.info("Sent notification for %s [%s]" % (context['product']['name'], context['name']))
