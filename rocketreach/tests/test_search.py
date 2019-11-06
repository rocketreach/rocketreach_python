import unittest

from rocketreach.person_gateway import PersonGateway, PersonSearch


class TestSearch(unittest.TestCase):
    def test_pagination(self):
        s = PersonSearch(None)
        s = s.params(2, 100)
        data = PersonGateway(None).to_search_body(s)
        expected = {
            'query': {},
            'start': 2,
            'page_size': 100,
        }
        self.assertDictEqual(data, expected)

    def test_query_name(self):
        s = PersonSearch(None)
        s = s.filter(name='John Doe')
        self.assertDictEqual({'name': ['John Doe']}, s.query)

    def test_query_2_names(self):
        s = PersonSearch(None)
        s = s.filter(name='John Doe')
        s = s.filter(name='Jane Doe')
        self.assertDictEqual({'name': ['John Doe', 'Jane Doe']}, s.query)

    def test_query_2_facets(self):
        s = PersonSearch(None)
        s = s.filter(name='John Doe')
        s = s.filter(current_title='CEO')
        self.assertDictEqual({'name': ['John Doe'], 'current_title': ['CEO']}, s.query)

    def test_query_2_facets_and_pagination(self):
        s = PersonSearch(None)
        s = s.filter(name='John Doe')
        s = s.filter(current_title='CEO')
        s = s.params(99, 25)
        data = PersonGateway(None).to_search_body(s)
        expected = {
            'query': {'name': ['John Doe'], 'current_title': ['CEO']},
            'start': 99,
            'page_size': 25,
        }
        self.assertDictEqual(expected, data)

    def test_query_exclude(self):
        s = PersonSearch(None)
        s = s.filter(name='John Doe')
        s = s.exclude(current_title='CEO')
        self.assertDictEqual({'name': ['John Doe'], 'exclude_current_title': ['CEO']}, s.query)
