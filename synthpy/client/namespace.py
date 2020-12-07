from .transport import Method
from .utils import NamespacedClient
from ..exceptions import BadRequest


class NamespaceClient(NamespacedClient):
    """Base class for the Namespace API.
    """

    def delete_collection(self, namespace, collection):
        request = self.transport.request(Method.DELETE)

        request.path.push(namespace).push(collection)

        return request.execute()

    def delete_namespace(self, namespace, erase=False):
        request = self.transport.request(Method.DELETE)

        request.path.push(namespace)

        request.param("erase", "true" if erase else "false")

        return request.execute()

    def get_namespaces(self):
        request = self.transport.request(Method.GET)

        return request.execute()

    def get_schema(self, namespace, collection=None, generation=None):
        request = self.transport.request(Method.GET)

        request.path.push(namespace)

        if collection:
            request.path.push(collection)

        if generation:
            request.params(generation=generation)

        request.path.push("_schema")

        return request.execute()

    def rollback_namespace(self, namespace, generation):
        request = self.transport.request(Method.PUT)

        request.path.push(namespace)

        request.params(generation=generation)

        request.path.push("_rollback")

        return request.execute()
