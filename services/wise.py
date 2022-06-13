import json
import uuid

import requests
from decouple import config
from werkzeug.exceptions import InternalServerError


class WiseService:
    def __init__(self):
        self.token = config('WISE_API_KEY')
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }
        self.base_url = config('WISE_URL')
        self.profile_id = self.get_profile_id()

    def get_profile_id(self):
        url = self.base_url + '/v1/profiles'
        resp = requests.get(url, headers=self.headers)
        if resp.status_code in (200, 201):
            return [el['id'] for el in resp.json() if el['type'] == 'personal'][0]
        raise InternalServerError('Payment provider is not available at the moment')

    def create_quote(self, amount):
        url = self.base_url + '/v2/quotes'
        data = {
          "sourceCurrency": "EUR",
          "targetCurrency": "EUR",
          "sourceAmount": amount,
          "targetAmount": None,
          "profile": self.profile_id,
        }

        resp = requests.post(url, data=json.dumps(data), headers=self.headers)
        if resp.status_code in (200, 201):
            return resp.json()['id']
        raise InternalServerError('Payment provider is not available at the moment')

    def create_recipient(self, full_name, iban):
        url = self.base_url + '/v1/accounts'
        data = {
            "currency": "EUR",
            "type": "iban",
            "profile": self.profile_id,
            "ownedByCustomer": True,
            "accountHolderName": full_name,
            "details": {
                "legalType": "PRIVATE",
                "iban": iban
            }
        }
        resp = requests.post(url, data=json.dumps(data), headers=self.headers)
        if resp.status_code in (200, 201):
            return resp.json()['id']
        raise InternalServerError('Payment provider is not available at the moment')

    def create_transfer(self, recipient_id, quote_id, custom_id):
        url = self.base_url + '/v1/transfers'
        data = {
            # "sourceAccount": <refund recipient account id>,
            "targetAccount": recipient_id,
            "quoteUuid": quote_id,
            "customerTransactionId": str(custom_id),
            "details": {}
         }
        resp = requests.post(url, data=json.dumps(data), headers=self.headers)
        if resp.status_code in (200, 201):
            return resp.json()['id']
        raise InternalServerError('Payment provider is not available at the moment')

    def fund_transfer(self, transfer_id):
        url = f'{self.base_url}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments'
        data = {
            "type": 'BALANCE'
        }
        resp = requests.post(url, data=json.dumps(data), headers=self.headers)
        if resp.status_code in (200, 201):
            return resp.json()['status']
        raise InternalServerError('Payment provider is not available at the moment')


if __name__ == '__main__':
    wise = WiseService()
    quote_id = wise.create_quote(20)
    recipient_id = wise.create_recipient('WiseTest Testing', 'BG18RZBB91550123456789')
    custom_id = uuid.uuid4()
    transfer_id = wise.create_transfer(recipient_id, quote_id, custom_id)
    status = wise.fund_transfer(transfer_id)
    print(status)