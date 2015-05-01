from django.core.management.base import NoArgsCommand

import requests

from webhook.utils import shopify_api


class Command(NoArgsCommand):
    help = 'List all active Shopify webhooks'

    def handle_noargs(self, **options):
        hooks = requests.get(shopify_api('/admin/webhooks.json')).content
        self.stdout.write(hooks)
