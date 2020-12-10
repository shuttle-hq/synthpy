from .transport import Method
from .utils import NamespacedClient, scoped
from ..exceptions import ImproperlyConfigured


class IngestClient(NamespacedClient):
    """Base class for the Ingest API.

    .. note::
        Do not construct this class directly. Access it from the root
        :class:`.Synth` client instead.

    Example:
        .. code-block:: python

           >>> from synthpy import Synth
           >>> client = Synth()
           >>> client.put_documents(namespace="my_namespace", collection="my_collection", document={"yes?": True})
    """

    @scoped("namespace")
    def put_documents(self, collection=None, document=None, batch=None, namespace=None):
        """Ingest one or more documents.

        This supports both individual and batch document ingestion. In
        general, batch is favored as it results in fewer individual
        API requests and allows ``synthd`` to optimize its internal
        updating of the collection's model.

        :param namespace: The name of the namespace we should ingest the document(s) to.
        :type namespace: str

        :param collection: The name of the collection we should ingest the document(s) to.
        :type collection: str

        :param document: The document we should ingest in the collection. This uses the API in individual ingestion mode.
        :type document: dict, optional

        :param batch: An iterable of documents we should ingest in the collection. This uses the API in batch mode.
        :type batch: Iterable[dict], optional

        .. note::
           Exactly one of ``document`` or ``batch`` must be set.

        """

        has_document = document is not None
        has_batch = batch is not None
        if has_document and has_batch or (not has_document and not has_batch):
            raise ImproperlyConfigured("batch, document", "exactly one of 'document' or 'batch' must be set")

        request = self.transport.request(Method.PUT)

        if not namespace or not collection:
            raise ImproperlyConfigured("namespace, collection", "'namespace' and 'collection' are required arguments")

        request.path.push(namespace).push(collection)

        if has_document:
            request.body(document=document)
        elif has_batch:
            request.body(batch=batch)

        return request.execute()
