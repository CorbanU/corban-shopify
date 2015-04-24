import factory
from mock import patch

from webhooks.models import Webhook


class WebhookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Webhook

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        with patch('requests.post') as mock:
            mock.return_value.status_code = 200
            mock.return_value.raise_for_status.return_value = None
            mock.return_value.raise_for_status()
            mock.return_value.json.return_value = {'webhook': {'id': 12345}}
            mock.return_value.json()
            return super(WebhookFactory, cls)._create(target_class, *args, **kwargs)
