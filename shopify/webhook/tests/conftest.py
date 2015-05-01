import os.path

import pytest

from webhook.utils import calculate_hmac


@pytest.fixture(scope='class')
def json(request):
    pwd = os.path.dirname(__file__)
    filename = getattr(request.cls, 'filename')
    with open(os.path.join(pwd, 'fixtures', filename)) as f:
        json = f.read()
    return json


@pytest.fixture(scope='class')
def hmac(json):
    return calculate_hmac(json)
