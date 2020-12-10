from .transport import Method
from .utils import NamespacedClient, scoped
from ..exceptions import BadRequest


class NamespaceClient(NamespacedClient):
    """Base class for the Namespace API.

    .. note::
        Do not construct this class directly. Access it from the root
        :class:`.Synth` client instead.

    Example:
        .. code-block:: python

           >>> from synthpy import Synth
           >>> client = Synth()
           >>> client.get_namespaces()
    """

    @scoped("namespace")
    def delete_collection(self, collection, namespace=None):
        """Delete a collection.

        Deleting a collection removes the collection from the
        namespace and advances the generation.

        .. note::
            This operation is reversible.

        Args:
            collection (str): the collection we want to delete.
            namespace (str, optional): the namespace we should delete
                the collection from. Can be omitted if previously set
                when initializing the client.
        """
        request = self.transport.request(Method.DELETE)

        request.path.push(namespace).push(collection)

        return request.execute()

    @scoped("namespace")
    def delete_namespace(self, erase=False, namespace=None):
        """Delete a namespace.

        .. warning::
            When `erase=True` is set, this operation is irreversible.

        Args:
            erase (bool, default to False): wether to erase the
                namespace, removing all information stored on it.
            namespace (str, optional): the namespace we should
                generate documents for. Can be omitted if previously
                set when initializing the client.
        """
        request = self.transport.request(Method.DELETE)

        request.path.push(namespace)

        request.param("erase", "true" if erase else "false")

        return request.execute()

    def get_namespaces(self):
        """List all namespaces.
        
        Retrieve a dict of all existing namespaces alongside their
        generation and last update timestamp.

        Returns:
            dict: A dictionary of namespaces. Values are dictionaries
            with keys 'current_generation' and 'last_updated_at'
        """
        request = self.transport.request(Method.GET)

        return request.execute()

    @scoped("namespace")
    def get_schema(self, field=None, generation=None, namespace=None):
        """Retrieve the schema of a single collection or all
        collections in a namespace.

        Args:
            field (str, optional): the `FieldRef` of the node we want
                to retrieve the schema of. If not specified, retrieves
                the schema of all collections in the namespace.
            generation (i32, optional): the generation for which we
                want to retrieve the schema. If not specified,
                retrieves the schema of the latest generation.
            namespace (str, optional): the namespace we should
                generate documents for. Can be omitted if previously
                set when initializing the client.

        Returns:
            dict: A schema dictionary.
        """
        request = self.transport.request(Method.GET)

        request.path.push(namespace)

        if field:
            request.param("at", field)

        if generation:
            request.param("generation", generation)

        request.path.push("_schema")

        return self.deserializer.load_coro(request.execute())

    @scoped("namespace")
    def rollback_namespace(self, generation, namespace=None):
        """Rollback to a specified namespace generation.

        .. note::
            This operation is reversible.

        Args:
            generation (i32, optional): the generation to rollback to.
            namespace (str, optional): the namespace we should
                generate documents for. Can be omitted if previously
                set when initializing the client.
        """
        request = self.transport.request(Method.PUT)

        request.path.push(namespace)

        request.params(generation=generation)

        request.path.push("_rollback")

        return request.execute()
