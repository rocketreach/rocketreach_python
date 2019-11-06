import unittest

from rocketreach.resource import Resource


class TestResource(unittest.TestCase):
    def test_fields(self):
        r = Resource(dict(a=1, b='test', c=None, d=0.5, e='?'))
        self.assertListEqual(r._resource_fields, ['a', 'b', 'c', 'd', 'e'])
        self.assertEqual(1, r.a)
        self.assertEqual('test', r.b)
        self.assertEqual(None, r.c)
        self.assertEqual(0.5, r.d)
        self.assertEqual('?', r.e)
