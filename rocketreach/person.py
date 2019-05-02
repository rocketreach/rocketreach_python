import requests
from requests import Response, Request


class Person(object):
    """
    Encapsulates a RocketReach Profile Lookup.

    Usage:
    >>> person = Person()
    >>> person.name = 'Michael Scott'
    >>> person.current_employer = 'Dunder Mifflin'
    >>> req = person.prepare_lookup_request()
    You can now use the prepared request to lookup the profile.
    """

    lookup_url = 'https://api.rocketreach.co/api/v2/person/lookup/'
    _flat_attrs_ = (
        'name', 'first_name', 'last_name', 'current_title', 'current_employer',
        'phones',
        'location', 'id', 'linkedin_url', 'profile_pic', 'status',
    )

    def __init__(self):
        self.found = None
        for attr in self._flat_attrs_:
            setattr(self, attr, None)
        self.emails = {
            'current_work': None,
            'current_personal': None,
            'other': None
        }

    def prepare_lookup_request(self) -> Request:
        req = requests.Request('GET', self.lookup_url)
        params = {}
        if self.id:
            params['id'] = self.id
        elif self.linkedin_url:
            params['linkedin_url'] = self.linkedin_url
        else:
            params['name'] = self.name
            params['current_employer'] = self.current_employer
        req.params = params
        return req

    def update_from_lookup_response(self, response: Response):
        if response.status_code == 404:
            self.found = False
        elif 200 <= response.status_code < 300:
            self.found = True
        if self.found:
            data = response.json()
            for attr in self._flat_attrs_:
                setattr(self, attr, data.get(attr))
            self.emails = {
                'current_work': data['current_work_email'],
                'current_personal': data['current_personal_email'],
                'other': data['emails'],
            }
        return self.found

    def __repr__(self):
        return '<%s: %s (%d) [%s]>' % (
            self.__class__.__name__, self.name, self.id or -1, 'found' if self.found else 'not found'
        )
