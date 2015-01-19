from configurations import values

from .base import Base


class Production(Base):
    SECRET_KEY = values.SecretValue()
    SHOPIFY_SHARED_SECRET = values.SecretValue()

    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', Base.TEMPLATE_LOADERS),
    )
