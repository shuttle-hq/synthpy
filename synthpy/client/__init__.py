from asyncio import get_event_loop

from .transport import Transport
from .ingest import IngestClient
from .generate import GenerateClient
from .namespace import NamespaceClient
from .override import OverrideClient


__all__ = [
    "Synth",
]


def run_in_event_loop(self, f):
    def __run_in_event_loop(*args, **kwargs):
        return self.event_loop.run_until_complete(f(*args, **kwargs))

    try:
        __run_in_event_loop.__doc__ = f.__doc__
    except AttributeError:
        pass

    return __run_in_event_loop


class Synth:
    """Main client for consuming the ``synthd`` API.

    This class can be used in one of two ways:

        1. By accessing each subclient separately and calling their
           respective API methods.
        2. By accessing these methods directly from this class.

    The only difference between 1. and 2. is that 1. will give you
    coroutines and so they have to be awaited in an event
    loop. Whereas 2. implicitly blocks by awaiting the coroutines in
    the default event loop. So if you need an async API then use
    1. but if you don't, use 2.

    Example:
        .. code-block: python

        >>> from synthpy import Synth
        >>> client = Synth()
        >>> await client.generate.get_documents(namespace="my_namespace")
        >>> client.get_documents(namespace="my_namespace")

    Attributes:
        ingest (IngestClient): The subclient for the Ingest API.
        generate (GenerateClient): The subclient for the Generate API.
        namespace (NamespaceClient): The subclient for the Namespace API.
        override (OverrideClient): The subclient for the Override API.

    Args:
        host (str): the :ref:`synthd <synthd>` node we should connect to. This
            should be a string of the form "{host}[:{port}]".
        **kwargs: extra arguments passed through to the inner
            :class:`.Transport` handler.

    """

    def __init__(self, host="localhost", **kwargs):
        self.transport = Transport(host, **kwargs)

        self.ingest = IngestClient(self)
        self.generate = GenerateClient(self)
        self.namespace = NamespaceClient(self)
        self.override = OverrideClient(self)

        dir_ = []

        for client_name in ["ingest", "generate", "namespace", "override"]:
            dir_.append(client_name)
            client = getattr(self, client_name)
            for member_name in dir(client):
                if member_name.startswith("__"):
                    continue

                member = getattr(client, member_name)

                if not callable(member):
                    continue

                setattr(self, member_name, run_in_event_loop(self, member))

                dir_.append(member_name)

        self._dir = dir_

        self.event_loop = get_event_loop()

    def __dir__(self):
        return self._dir

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.event_loop.run_until_complete(self.transport.session.close())
