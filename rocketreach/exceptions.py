class ExceptionCode:
    InvalidApiKey = 'invalid_api_key'
    PermissionDenied = 'permission_denied'
    InvalidParameters = 'invalid_parameters'
    NotFound = 'not_found'
    Other = 'other'


class RocketReachException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

    def __str__(self):
        return self.message


class NotFoundException(RocketReachException):
    pass


class RejectedException(RocketReachException):
    pass
