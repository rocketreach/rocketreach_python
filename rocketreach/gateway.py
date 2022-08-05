from json import JSONDecodeError
from typing import NamedTuple, Union

import requests
from requests import Request, Response

from rocketreach.account_gateway import AccountGateway
from rocketreach.exceptions import RejectedException, ExceptionCode
from rocketreach.person_gateway import PersonGateway
from rocketreach.result import ErrorResult, SuccessfulResult


class GatewayEnvironment:
    Production = 'production'
    Development = 'development'
    Sandbox = 'sandbox'


class GatewayConfig(NamedTuple):
    api_key: str
    environment: str = GatewayEnvironment.Production
    version: int = 2
    host: str = None
    port: int = None
    proto: str = None


class Gateway:
    sandbox_api_key = '3e7k0123456789abcdef0123456789abcdef'

    def __init__(self, config: GatewayConfig=None, api_key=None):
        if config is None:
            config = GatewayConfig(api_key=api_key)
        self.session = requests.Session()
        self.api_key = config.api_key

        if config.environment == GatewayEnvironment.Production:
            self.host = 'api.rocketreach.co'
            self.port = 443
            self.proto = 'https'
        elif config.environment == GatewayEnvironment.Development:
            self.host = 'localhost'
            self.port = 8000
            self.proto = 'http'
        elif config.environment == GatewayEnvironment.Sandbox:
            self.api_key = self.sandbox_api_key
            self.host = 'api.rocketreach.co'
            self.port = 443
            self.proto = 'https'
        if config.host:
            self.host = config.host
        if config.port:
            self.port = config.port
        if config.proto:
            self.proto = config.proto
        self.version = None
        self.url_prefix = None
        self.set_version(config.version)

        self.person = PersonGateway(self)
        self.account = AccountGateway(self)

    def get_headers(self):
        return {
            'Api-Key': self.api_key
        }

    def set_version(self, version):
        self.version = int(version)
        self.url_prefix = f'{self.proto}://{self.host}:{self.port}'
        if self.version == 1:
            self.url_prefix = f'{self.url_prefix}/v1/api'
        else:
            self.url_prefix = f'{self.url_prefix}/api/v2'

    def get_url(self, path: str):
        path = path.rstrip('/').lstrip('/')
        return f'{self.url_prefix}/{path}'

    def preflight(self, req: Request):
        req.headers = self.get_headers()

    def post_flight(self, resp: Response):
        pass

    def _get_error_message(self, response):
        try:
            data = response.json()
        except JSONDecodeError:
            data = {}
        if 'detail' in data:
            return data['detail']
        if 'error' in data:
            return data['error']
        else:
            error_list = []
            for field_name, v in data.items():
                if isinstance(v, list):
                    reason = ','.join(v)
                else:
                    reason = v
                error_list.append(f'`{field_name}` {reason}.')
            if error_list:
                return ' '.join(error_list)
            return 'Unknown error occurred'

    def send(self, req: Request) -> Union[ErrorResult, SuccessfulResult]:
        self.preflight(req)
        preq = req.prepare()
        res = self.session.send(preq)
        self.post_flight(res)
        if res.status_code >= 400:
            error_msg = self._get_error_message(res)
            if res.status_code in (401, ):
                raise RejectedException(error_msg, ExceptionCode.InvalidApiKey)
            elif res.status_code in (403, ):
                raise RejectedException(error_msg, ExceptionCode.PermissionDenied)

            result = ErrorResult(req, res)
            result.message = error_msg
        else:
            result = SuccessfulResult(req, res)
        return result


sandbox_gateway = Gateway(
    GatewayConfig(api_key='', environment=GatewayEnvironment.Sandbox)
)

dev_gateway = Gateway(
    GatewayConfig(api_key=Gateway.sandbox_api_key, environment=GatewayEnvironment.Development)
)
