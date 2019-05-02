import requests
from requests import Request, Response

from .person import Person


class Gateway(object):
    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.headers = {
            'Api-Key': api_key,
        }

    def lookup(self, person: Person):
        req = person.prepare_lookup_request()
        response = self.send(req)
        person.update_from_lookup_response(response)

    def preflight(self, req: Request):
        req.headers = self.headers

    def post_flight(self, resp: Response):
        pass

    def send(self, req: Request) -> Response:
        self.preflight(req)
        preq = req.prepare()
        response = self.session.send(preq)
        self.post_flight(response)
        return response
