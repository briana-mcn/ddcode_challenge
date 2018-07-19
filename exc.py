class BaseError(Exception):
    pass


class HTTPError(BaseError):
    """Exception class for errors unexpectedly raised from API requests"""
    pass


class VCSManagerError(BaseError):
    """Base exception class for errors raised within the program"""
    pass


class RequestError(VCSManagerError):
    """Exceptions class for invalid incoming requests made to the app"""
    pass
