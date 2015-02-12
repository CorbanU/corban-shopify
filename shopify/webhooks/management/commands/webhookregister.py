from django.core.management.base import NoArgsCommand

from webhooks.models import Webhook


class Command(NoArgsCommand):
    help = 'Register all created Shopify webhooks'

    def handle_noargs(self, **options):
        Webhook.objects.register()
