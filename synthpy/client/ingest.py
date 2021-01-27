from .transport import Method
from .utils import NamespacedClient, scoped
from ..exceptions import ImproperlyConfigured
from ..model import Model


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
    def put_documents(
        self, collection=None, document=None, batch=None, hint=None, namespace=None
    ):
        """Ingest one or more documents.

        This supports both individual and batch document ingestion. In
        general, batch is favored as it results in fewer individual
        API requests and allows ``synth`` to optimize its internal
        updating of the collection's model.

        :param namespace: The name of the namespace we should ingest the document(s) to.
        :type namespace: str

        :param collection: The name of the collection we should ingest the document(s) to.
        :type collection: str

        :param document: The document we should ingest in the collection. This uses the API in individual ingestion mode.
        :type document: dict, optional

        :param batch: An iterable of documents we should ingest in the collection. This uses the API in batch mode.
        :type batch: Iterable[dict], optional

        :param hint: Hint about the content of the ingest. If specified, must follow the same format as the `override` parameter of :meth:`put_override <synthpy.client.override.OverrideClient.put_override>`.
        :type hint: dict, optional

        .. note::
           Exactly one of ``document`` or ``batch`` must be set.

        """

        has_document = document is not None
        has_batch = batch is not None
        if has_document and has_batch or (not has_document and not has_batch):
            raise ImproperlyConfigured(
                "batch, document", "exactly one of 'document' or 'batch' must be set"
            )

        request = self.transport.request(Method.PUT)

        if not namespace or not collection:
            raise ImproperlyConfigured(
                "namespace, collection",
                "'namespace' and 'collection' are required arguments",
            )

        request.path.push(namespace).push(collection)

        kwargs = {}

        if has_document:
            kwargs.update({"document": document})
        elif has_batch:
            kwargs.update({"batch": batch})

        if hint is not None:
            if isinstance(hint, Model):
                hint = hint._into_content()._into_repr()
            kwargs.update({"hint": hint})

        request.body(**kwargs)

        return request.execute()
