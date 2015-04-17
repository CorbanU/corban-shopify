import os.path

import pytest

from webhooks.utils import calculate_hmac


@pytest.fixture(scope='class')
def json(request):
    filename = getattr(request.cls, 'filename')
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        json = f.read()
    return json


@pytest.fixture(scope='class')
def hmac(json):
    return calculate_hmac(json)
