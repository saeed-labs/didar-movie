import requests

from django.conf import settings


class ZarinpalGateway:
    API_URL = "https://api.zarinpal.com/pg/v4/payment"
    GATEWAY_URL = "https://www.zarinpal.com/pg/StartPay"

    SANDBOX_API_URL = "https://sandbox.zarinpal.com/pg/v4/payment"
    SANDBOX_GATEWAY_URL = "https://sandbox.zarinpal.com/pg/StartPay"

    def __init__(self):
        if settings.ZARINPAL_SANDBOX:
            self.api_url = self.SANDBOX_API_URL
            self.gateway_url = self.SANDBOX_GATEWAY_URL
        else:
            self.api_url = self.API_URL
            self.gateway_url = self.GATEWAY_URL

        self.merchant_id = settings.ZARINPAL_MERCHANT_ID

    def request_payment(self, amount, description, callback_url, mobile=None, email=None):
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "description": description,
            "callback_url": callback_url,
        }

        metadata = {}

        if mobile:
            metadata["mobile"] = mobile

        if email:
            metadata["email"] = email

        if metadata:
            data["metadata"] = metadata

        response = requests.post(
            f"{self.api_url}/request.json",
            json=data,
            headers={
                "Content-Type": "application/json",
            },
            timeout=15,
        )

        response.raise_for_status()

        result = response.json()

        return result

    def get_payment_url(self, authority):
        return f"{self.gateway_url}/{authority}"

    def verify_payment(self, amount, authority):
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority,
        }

        response = requests.post(
            f"{self.api_url}/verify.json",
            json=data,
            headers={"Content-Type": "application/json"}, timeout=15
        )

        response.raise_for_status()

        return response.json()



