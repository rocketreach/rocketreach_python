from collections import defaultdict


class PersonSearch:
    def __init__(self, person_gateway):
        self.gateway = person_gateway
        self.start = 1
        self.size = 10
        self._facets = defaultdict(list)

    @property
    def query(self):
        return dict(self._facets)

    def __copy__(self):
        return self._clone()

    def _clone(self):
        s = self.__class__(self.gateway)
        s._facets = self._facets.copy()
        return s

    def filter(self, **kwargs):
        s = self._clone()
        for k, v in kwargs.items():
            s._facets[k].append(v)
        return s

    def exclude(self, **kwargs):
        s = self._clone()
        for k, v in kwargs.items():
            s._facets[f'exclude_{k}'].append(v)
        return s

    def params(self, start=None, size=None):
        s = self._clone()
        if start:
            s.start = start
        if size:
            s.size = size
        return s

    def execute(self):
        return self.gateway.execute_search(self)
