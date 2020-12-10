__all__ = ["SynthException", "TransportError", "BadRequest"]


class SynthException(Exception):
    """Base class for all exceptions raised by this package."""


class ImproperlyConfigured(SynthException):
    """Exception raised when user-defined values passed to the client are
    improper or invalid.

    """

    @property
    def value(self):
        return self.args[0]

    @property
    def info(self):
        return self.args[1]


class TransportError(SynthException):
    """Exception raised when synthd responds with a status code above 400,
    or when a connection error arises.
    """

    def __init__(self, kind=None, msg=None):
        self.kind = kind
        self.msg = msg
        Exception.__init__(self)

    def __str__(self):
        if self.msg:
            return ": ".join(self.msg)
        else:
            return "an unspecified error occured: this is usually due to a programming error in the client or the daemon."


class BadRequest(TransportError):
    """Exception representing a 400 status code."""

    @property
    def reason(self):
        return self.msg.get(0)


class SerializationError(TransportError):
    """Exception representing a 422 status code."""


class NotFoundError(TransportError):
    """Exception representing a 404 status code."""


class InternalServerError(TransportError):
    """Exception representing a 500 status code."""


HTTP_EXCEPTIONS = {400: BadRequest, 404: NotFoundError, 500: InternalServerError, 422: SerializationError}
