import re
import time
from typing import Union

import requests

from rocketreach.exceptions import RocketReachException
from rocketreach.person import Person, PersonCollection
from rocketreach.person_search import PersonSearch
from rocketreach.result import ErrorResult, SuccessfulResult


class PersonLookupStatus:
    Complete = 'complete'
    Progress = 'progress'
    Searching = 'searching'
    Queued = 'queued'


class PersonGateway:
    default_polling_interval = 5

    def __init__(self, gateway):
        self.gateway = gateway
        self.resource_paths = {
            1: {
                'lookup': 'lookupProfile',
                'check_status': 'checkStatus',
                'search': 'search',
            },
            2: {
                'lookup': 'person/lookup',
                'check_status': 'person/checkStatus',
                'search': 'search',
            }
        }

    def get_url(self, endpoint_name):
        path = self.resource_paths[self.gateway.version][endpoint_name]
        return self.gateway.get_url(path)

    def _prepare_lookup_request(self) -> requests.Request:
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

    def poll_until_complete(self, lookups, interval=None):
        if not interval:
            interval = self.default_polling_interval
        complete_lookups = {}
        failures = 0
        while True:
            poll_ids = set()
            for person in lookups:
                if person.status != PersonLookupStatus.Complete:
                    poll_ids.add(person.id)
                    complete_lookups[person.id] = person
            result = self.check_status(poll_ids)
            if result.is_success:
                lookups = result.people
            else:
                failures += 1
            if not poll_ids:
                break
            time.sleep(interval)

        res = PersonCollection()
        # Get the lookups back in the same order
        for person in lookups:
            res.append(complete_lookups[person.id])
        return res

    def _execute_lookup(self, req, block):
        result = None
        while not result or not result.is_success:
            result = self.gateway.send(req)
            if result.is_success:
                person = Person(result.data)
                if block:
                    result.person = self.poll_until_complete([person])
                else:
                    result.person = person
                return result
            else:
                if result.response.status_code == 429:
                    m = re.search(r'Expected available in (\d+) second', result.message).group(1)
                    if m:
                        wait = int(m)
                    else:
                        wait = 2
                    if block:
                        time.sleep(wait)
                    else:
                        raise RocketReachException(f'Lookups are rate-limited for {wait} seconds.')
                else:
                    return result

    def lookup(self, person_id=None, linkedin_url=None, block=True, extras={}) -> Union[ErrorResult, SuccessfulResult]:
        if person_id:
            extras['id'] = int(person_id)
        if linkedin_url:
            extras['linkedin_url'] = linkedin_url
        req = requests.Request(method='GET',
                               url=self.get_url('lookup'),
                               params=extras)
        result = self._execute_lookup(req, block)
        return result

    def check_status(self, ids):
        if isinstance(ids, tuple) or isinstance(ids, list):
            ids = [ids]
        req = requests.Request(method='GET',
                               url=self.get_url('check_status'),
                               params={'ids': ids})
        result = self.gateway.send(req)
        if result.is_success:
            result.people = PersonCollection()
            for item in result.data:
                result.people.append(Person(item))
        return result

    def search(self):
        s = PersonSearch(self)
        return s

    def to_search_body(self, search: PersonSearch) -> dict:
        query = search.query
        return {
            'query': query,
            'start': search.start,
            'page_size': search.size,
        }

    def execute_search(self, search):
        if self.gateway.version == 1:
            query = search.query
            req = requests.Request(method='GET',
                                   url=self.get_url('search'),
                                   params=query)
        else:
            data = self.to_search_body(search)
            req = requests.Request(method='POST',
                                   url=self.get_url('search'),
                                   json=data)
        result = self.gateway.send(req)
        if result.is_success:
            result.people = PersonCollection()
            for entry in result.data['profiles']:
                result.people.append(Person(entry))
        return result
