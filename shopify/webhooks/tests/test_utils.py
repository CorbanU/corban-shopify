import os.path

import pytest

from webhooks.utils import calculate_hmac
from webhooks.utils import verify_webhook


@pytest.fixture(scope='module')
def json():
    filename = 'fixtures/orders-paid.json'
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        json = f.read()
    return json


@pytest.fixture(scope='module')
def hmac():
    return calculate_hmac(json())


class TestUtils:
    def test_verify_webhook_valid(self, json, hmac):
        assert verify_webhook(json, hmac)

    def test_verify_webhook_invalid(self, json, hmac):
        assert not verify_webhook('invalid data', hmac)
        assert not verify_webhook(json, 'invalid sha256')
