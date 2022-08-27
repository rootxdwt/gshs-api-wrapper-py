class BaseException(Exception):
    """
    Base Exception
    """

class NetworkException(BaseException):
    """
    An Error Occured While Connecting To The Server
    """

class ResponseParseException(BaseException):
    """
    An Error Occured While Parsing Response Data
    """

class RequestParseException(BaseException):
    """
    An Error Occured While Parsing Requested Data
    """

class AuthenticationException(BaseException):
    """
    An Error Occured While Parsing Requested Data
    """