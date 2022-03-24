from collections import defaultdict
from collections.abc import Iterable
from .exceptions import RocketReachException, ExceptionCode


PAGE_LIMIT = 10000

class PersonSearchPaginator:
    def __init__(self, search):
        self.search = search
    
    def __iter__(self):
        result = None
        search = self.search
        if hasattr(search, 'limit'):
            limit = search.limit
            del search.limit
        else:
            limit = None
        while True:
            result = search.execute()
            if result.is_success:
                if limit is not None:
                    if len(result.people) >= limit:
                        yield from result.people[:limit]
                        return
                    limit -= len(result.people)
                    if limit < 0:
                        return
                yield from result.people
            else:
                return
            search = search.params(start=result.data['pagination']['next'])
            

class PersonSearch:
    def __init__(self, person_gateway):
        self.gateway = person_gateway
        self.start = 1
        self.size = 10
        self._options = {}
        self._facets = defaultdict(list)

    @property
    def query(self):
        return dict(self._facets)

    def __copy__(self):
        return self._clone()

    def _clone(self):
        s = self.__class__(self.gateway)
        s._facets = self._facets.copy()
        s.start = self.start
        s.size = self.size
        s._options = self._options.copy()
        return s

    def _make_iterable(self, arg):
        if isinstance(arg, str):
            result = [arg]
        elif isinstance(arg, Iterable):
            result = arg
        else:
            result = [arg]
        return result

    def filter(self, **kwargs):
        s = self._clone()
        for k, v in kwargs.items():
            s._facets[k].extend(self._make_iterable(v))
        return s

    def exclude(self, **kwargs):
        s = self._clone()
        for k, v in kwargs.items():
            s._facets[f'exclude_{k}'].extend(self._make_iterable(v))
        return s

    def get_options(self) -> dict:
        return self._options

    def options(self, **kwargs):
        s = self._clone()
        s._options.update(kwargs)
        return s

    def params(self, start=None, size=None):
        s = self._clone()
        if start:
            s.start = start
        if size:
            s.size = size
        return s

    def __getitem__(self, key):
        if isinstance(key, slice):
            s = self._clone()
            if key.step:
                raise ValueError(f'Invalid slice, step is not supported.')
            if key.start:
                s.start = key.start + 1
            else:
                s.start = 1
            if key.stop:
                s.limit = key.stop + 1 - s.start
            else:
                s.limit = None
            return s
        elif isinstance(key, int):
            s = self._clone()
            s.start = key + 1
            s.size = 1
            result = s.execute()
            if result.is_success:
                return result.people[0]
            else:
                raise RocketReachException(result.message, ExceptionCode.NotFound)
        elif isinstance(key, tuple):
            raise NotImplementedError('Tuple as index')
        else:
            raise TypeError(f'Invalid argument type: {type(key)}')

    def execute(self):
        if hasattr(self, 'limit'):
            raise RuntimeException('Sliced queries cannot be executed. Make sure you call `.iterator()`!')
        return self.gateway.execute_search(self)

    def iterator(self):
        return PersonSearchPaginator(self)

