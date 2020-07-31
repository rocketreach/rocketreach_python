from pprint import pformat


class Resource:
    def __init__(self, attributes={}):
        self._resource_fields = []
        for key, val in attributes.items():
            setattr(self, key, val)
            self._resource_fields.append(key)

    def __str__(self):
        details = ', '.join("%s: %r" % (field_name, getattr(self, field_name))
                                for field_name in self._resource_fields
                                    if hasattr(self, field_name))

        if len(details) > 77:
            details = f'{details[:77]}...'
        return f'<{self.__class__.__name__} {details} {id(self)}'

    def to_dict(self):
        result = {}
        for field_name in self._resource_fields:
            if hasattr(self, field_name):
                result[field_name] = getattr(self, field_name)
        return result

    def __repr__(self):
        return pformat(self.to_dict())

