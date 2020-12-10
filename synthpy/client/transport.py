import logging
from urllib.parse import urljoin

from aiohttp import ClientResponse, ClientSession
from aiohttp.client_exceptions import ContentTypeError
from yarl import URL

from ..exceptions import ImproperlyConfigured, HTTP_EXCEPTIONS, InternalServerError
import json

from .encoder import Encoder, json_serialize


__all__ = ["Transport", "Method"]


SYNTHD_DEFAULT_PORT = 8182


logger = logging.getLogger("synthpy")


class Method:
    GET = "get"
    PUT = "put"
    DELETE = "delete"


# Not sure why we are not using a URL lib here

class Path:
    def __init__(self):
        self._path = "/"

    def push(self, part):
        self._path = urljoin(f"{self._path}/", part)
        return self

    def __str__(self):
        return self._path



class RequestBuilder:
    """Builder for ``synthd`` API requests.
    """

    def __init__(self, method, transport):
        self.transport = transport

        self.method = method

        self.path = Path()

        self._body = None
        self._params = {}

    def body(self, **kwargs):
        body = kwargs
        try:
            json.dumps(body, cls=Encoder)
        except TypeError or ValueError or OverflowError as e:
            raise e
        self._body = body
        return self

    def param(self, key, value):
        self._params[key] = value
        return self

    def params(self, **kwargs):
        for key, value in kwargs.items():
            self.param(key, value)
        return self

    def execute(self):
        return self.transport.execute(self)


class Transport:
    """Low-level internal transport handler used by API clients.
    """

    def __init__(self, host, defaults={}, enable_tls=False):
        split = host.split(":")
        if len(split) == 1:
            host = split[0]
            port = SYNTHD_DEFAULT_PORT
        elif len(split) == 2:
            host, port = split
        else:
            raise ImproperlyConfigured("host", "not of the form '{host}[:{port}]'")

        if enable_tls:
            raise NotImplementedError(
                "TLS is not supported by the python client implementation yet."
            )
        self.enable_tls = enable_tls

        self.defaults = defaults
        self.active = {}

        scheme = "https" if self.enable_tls else "http"
        self.base_url = URL.build(scheme=scheme, host=host, port=port)

        self.session = ClientSession(json_serialize=json_serialize)

    def get_default(self, name):
        return self.defaults.get(name)

    def request(self, method):
        """Create a new :class:`.RequestBuilder`.
        """
        return RequestBuilder(method, transport=self)

    def _url_from_path(self, path: Path) -> URL:
        return self.base_url.with_path(str(path))

    async def execute(self, request):
        """Coroutine for sending a request to the ``synthd`` host and handling
        the response.

        Args:
            request (:class:`.RequestBuilder`): The request we should execute.
        """
        fn = getattr(self.session, request.method)

        url = self._url_from_path(request.path)
        body = request._body
        params = request._params

        logger.info(
            f"request: method={request.method} url={url} body={body}"
        )
        resp = await fn(url=url, json=body, params=params)

        try:
            body = await resp.json()
        except ContentTypeError:
            body = None

        if resp.status >= 400:
            logger.info(f"response: status={resp.status} body={body}")
            cls = HTTP_EXCEPTIONS.get(resp.status, InternalServerError)
            body = {} if not body else body
            print(resp.status)
            raise cls(**body)
        else:
            return body
