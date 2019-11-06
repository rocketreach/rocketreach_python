from typing import Union

import requests

from rocketreach.account import Account
from rocketreach.exceptions import RejectedException
from rocketreach.result import ErrorResult, SuccessfulResult


class AccountGateway:
    def __init__(self, gateway):
        self.gateway = gateway

    def get(self) -> Union[ErrorResult, SuccessfulResult]:
        req = requests.Request(method='GET', url=self.gateway.get_url('account'))
        result = self.gateway.send(req)
        if result.is_success:
            result.account = Account(result.data)
        return result

    def change_key(self, current_key) -> Union[ErrorResult, SuccessfulResult]:
        data = {'api_key': current_key}
        req = requests.Request(method='POST', data=data, url=self.gateway.get_url('account/key'))
        result = self.gateway.send(req)
        if result.is_success:
            result.new_api_key = result.data['api_key']
        else:
            raise RejectedException()
        return result
