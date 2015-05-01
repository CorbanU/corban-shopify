from django.core.management.base import NoArgsCommand

import requests

from webhook.utils import shopify_api


class Command(NoArgsCommand):
    help = 'Display count of active Shopify webhooks'

    def handle_noargs(self, **options):
        count = requests.get(shopify_api('/admin/webhooks/count.json')).content
        self.stdout.write(count)
