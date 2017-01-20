from django.apps import AppConfig


class WebhookConfig(AppConfig):
    name = 'shopify.webhook'
    verbose_name = 'Webhook'

    def ready(self):
        pass
