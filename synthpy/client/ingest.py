from .transport import Method
from .utils import NamespacedClient
from ..exceptions import BadRequest


class IngestClient(NamespacedClient):
    """Base class for the Ingest API.

    **Do not construct this class directly**. Instead, access it from
    the root :class:`.Synth` client.

    Example:
        .. code-block:: python

           from synthpy import Synth
           client = Synth()
           client.ingest.put_documents("my_namespace", "my_collection", document={"yes?": True})
    """

    def put_documents(self, namespace, collection, document=None, batch=None):
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

        if document and batch or (not document and not batch):
            raise BadRequest("exactly one of 'document' or 'batch' must be set")

        request = self.transport.request(Method.PUT)

        request.path.push(namespace).push(collection)

        if document:
            request.body(document=document)
        elif batch:
            request.body(batch=batch)

        return request.execute()
