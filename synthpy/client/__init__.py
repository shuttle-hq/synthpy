from .transport import Transport
from .ingest import IngestClient
from .generate import GenerateClient
from .namespace import NamespaceClient
from .override import OverrideClient
from .augmentation import  AugmentationClient


__all__ = ["Synth"]


class Synth:
    """Client for consuming the ``synthd`` API.

    :ivar IngestClient ingest: The subclient for the Ingest API.
    :ivar GenerateClient generate: The subclient for the Generate API.
    """
    def __init__(self, host="localhost", **kwargs):
        """Create a new API client.

        :param host: The ``synthd`` node we should connect to. This should be a string of the form "{host}[:{port}]".
        :type host: str

        :param kwargs: Extra arguments passed through to the inner :class:`.Transport` handler.
        :type kwargs: dict
        """
        self.transport = Transport(host, **kwargs)

        self.ingest = IngestClient(self)
        self.generate = GenerateClient(self)
        self.namespace = NamespaceClient(self)
        self.override = OverrideClient(self)
        self.augmentation = AugmentationClient(self)
