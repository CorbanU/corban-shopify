from optparse import make_option

from django.core.management.base import BaseCommand

import requests

from webhooks.utils import shopify_api


class Command(BaseCommand):
    args = '<request>'
    help = 'Execute a given Shopify API request'
    option_list = BaseCommand.option_list + (
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Send a DELETE request'),
        make_option('--post',
            action='store_true',
            dest='post',
            default=False,
            help='Send a POST request'),
        make_option('--put',
            action='store_true',
            dest='put',
            default=False,
            help='Send a PUT request'),
    )

    def handle(self, *args, **options):
        if args:
            request = args[0]
            if options['delete']:
                result = requests.delete(shopify_api(request)).content
            elif options['post']:
                result = requests.post(shopify_api(request)).content
            elif options['put']:
                result = requests.put(shopify_api(request)).content
            else:
                result = requests.get(shopify_api(request)).content
            self.stdout.write(result)
        else:
            self.stdout.write('No request string provided')
