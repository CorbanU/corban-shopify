import os.path

import pytest

from webhooks.utils import calculate_hmac


@pytest.fixture(scope='module')
def json():
    filename = 'fixtures/orders-paid.json'
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        json = f.read()
    return json


@pytest.fixture(scope='module')
def hmac():
    return calculate_hmac(json())
