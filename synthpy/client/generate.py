from .utils import NamespacedClient
from .transport import Method


class GenerateClient(NamespacedClient):
    """Base class for the Generate API.

    **Do not construct this class directly**. Instead, access it from
    the root :class:`.Synth` client.

    Example:
        .. code-block:: python

           from synthpy import Synth
           client = Synth()
           client.generate.get_documents("my_namespace", "my_collection", size=10)
    """

    def get_documents(self, namespace, collection=None, size=1):
        """Generate one or more synthetic documents.

        Args:
            namespace (str): The namespace we should generate documents for.
            collection (str, optional): the collection we want to
                generate documents for.  If not set, we will generate
                documents from all collections belonging to the
                namespace.
            size (int, defaults to 1): the target number of documents
                to generate.

        .. warning::
           There is no guarantee you will get
           *exactly* ``size`` documents in the output. This is because some
           constraints (such as primary key/foreign key constraints) are
           incompatible with that exactness. You are guaranteed, however,
           to get *at least* that number of documents.
        """

        request = self.transport.request(Method.GET)

        request.path.push(namespace)

        if collection:
            request.path.push(collection)

        request.path.push("_sample")

        request.params(size=size)

        return request.execute()
