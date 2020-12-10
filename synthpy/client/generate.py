from .utils import NamespacedClient, scoped
from .transport import Method


class GenerateClient(NamespacedClient):
    """Base class for the Generate API.

    .. note::
        Do not construct this class directly. Access it from the root
        :class:`.Synth` client instead.

    Example:
        .. code-block:: python

           >>> from synthpy import Synth
           >>> client = Synth()
           >>> client.get_documents(namespace="my_namespace", size=10)
    """

    @scoped("namespace")
    def get_documents(self, collection=None, size=1, namespace=None):
        """Generate one or more synthetic documents.

        Args:
            collection (str, optional): the collection we want to
                generate documents for.  If not set, we will generate
                documents for all collections belonging to the
                namespace.
            size (int, defaults to 1): the target number of documents
                to generate.
            namespace (str, optional): the namespace we should
                generate documents for. Can be omitted if previously
                set when initializing the client.

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
