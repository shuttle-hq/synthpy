from .transport import Method
from .utils import NamespacedClient
from ..exceptions import BadRequest


class OverrideClient(NamespacedClient):
    """Base class for the Override API."""

    def put_override(self, namespace, field, override):
        request = self.transport.request(Method.PUT)

        request.path.push(namespace).push("_override")

        request.body(field=field, override=override)

        return request.execute()

    def set_optional(self, namespace, field, optional):
        request = self.transport.request(Method.PUT)

        request.path.push(namespace).push("_optionalise")

        request.body(field=field, optional=optional)

        return request.execute()

    def optionalise(self, namespace, field):
        return self.set_optional(namespace, field, optional=True)

    def unoptionalise(self, namespace, field):
        return self.set_optional(namespace, field, optional=False)
