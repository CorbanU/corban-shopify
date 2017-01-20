from django.apps import AppConfig


class NotificationConfig(AppConfig):
    name = 'shopify.notification'
    verbose_name = 'Notification'

    def ready(self):
        pass
