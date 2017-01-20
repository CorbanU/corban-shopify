from django.apps import AppConfig


class ProductConfig(AppConfig):
    name = 'shopify.product'
    verbose_name = 'Product'

    def ready(self):
        pass
