from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'shopify.user'
    verbose_name = 'User'

    def ready(self):
        pass
