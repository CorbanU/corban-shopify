from webhooks.utils import verify_webhook


class TestUtils:
    def test_verify_webhook_valid(self, json, hmac):
        assert verify_webhook(json, hmac)

    def test_verify_webhook_invalid(self, json, hmac):
        assert not verify_webhook('invalid data', hmac)
        assert not verify_webhook(json, 'invalid sha256')
