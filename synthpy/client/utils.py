class NamespacedClient:
    """Base class for a section of the ``synthd`` client API.

    Individual APIs should inherit from ``NamespacedClient`` to
    interop easily with the root user-facing client object ``Synth``.
    """

    def __init__(self, client):
        self.client = client

    @property
    def transport(self):
        return self.client.transport
