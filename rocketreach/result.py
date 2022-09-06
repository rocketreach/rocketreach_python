from json import JSONDecodeError

import requests


class SuccessfulResult:
    def __init__(self, request: requests.Request, response: requests.Response):
        self.request = request
        self.response = response
        self.data = response.json()

    @property
    def is_success(self):
        return True

    def __repr__(self):
        results = set(self.__dict__.keys()).difference(['request', 'response', 'data'])
        result_name = ', '.join([getattr(self, r).__class__.__name__ for r in results])
        return f'<{self.__class__.__name__} of {result_name}>'


class ErrorResult:
    def __init__(self, request: requests.Request, response: requests.Response):
        self.request = request
        self.response = response
        try:
            self.errors = response.json()
        except JSONDecodeError:
            self.errors = {}
        self.message = None

    @property
    def is_success(self):
        return False
