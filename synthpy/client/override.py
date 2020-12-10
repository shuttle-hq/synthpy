from .transport import Method
from .utils import NamespacedClient, scoped, canonicalize
from ..exceptions import BadRequest
from ..model import Model

import logging


logger = logging.getLogger("synthpy")


class OverrideClient(NamespacedClient):
    """Base class for the Namespace API.

    .. note::
        Do not construct this class directly. Access it from the root
        :class:`.Synth` client instead.

    Example:
        .. code-block:: python

           >>> from synthpy import Synth
           >>> client = Synth()
           >>> client.delete_override("my_collection.content.a_field")
    """

    @scoped("namespace")
    def put_override(self, field, override, depth=None, namespace=None):
        """Override a schema node.

        Args:
            field (str): the `FieldRef` of the field node to
                override.
            override (dict or Model): the override to apply to
                the specified field.
            depth (unsigned int, optional): until what depth is the
                override merging with the existing model. If not
                specified, the override is a merge at all depths. If
                set to `0`, the operation will replace the schema
                entry at `field` with the given `override`.
            namespace (str, optional): Can be omitted if previously
                set when initializing the client.
        """
        request = self.transport.request(Method.PUT)

        request.path.push(namespace).push("_override")

        if isinstance(override, Model):
            override = override._into_content()._into_repr()
        elif isinstance(override, dict):
            override = override
        else:
            raise ValueError("'override' must be either a 'dict' or a 'Model'")

        override = canonicalize(override)

        logger.debug(f"override={override}")

        request.body(at=field, override=override)

        if depth is not None:
            request.params(depth=depth)

        return request.execute()

    @scoped("namespace")
    def delete_override(self, field, namespace=None):
        """Delete a schema node.

        Args:
            field (str): the `FieldRef` of the field node to
                delete.
            namespace (str, optional): Can be omitted if previously
                set when initializing the client.
        """
        request = self.transport.request(Method.DELETE)

        request.path.push(namespace).push("_override")

        request.params(at=field)

        return request.execute()

    @scoped("namespace")
    def set_optional(self, field, optional, namespace=None):
        """Make a field node optional or required.

        Args:
            field (str): the `FieldRef` of the field node to
                unoptionalise.
            optional (bool): wether to make the field optional or
                required.
            namespace (str, optional): Can be omitted if previously
                set when initializing the client.
        """
        request = self.transport.request(Method.PUT)

        request.path.push(namespace).push("_optionalise")

        request.body(at=field, optional=optional)

        return request.execute()

    @scoped("namespace")
    def optionalise(self, field, namespace):
        """Make a field node optional (not required)

        Exactly the same as `OverrideClient.set_optional(field, optional=True)`.

        Args:
            field (str): the `FieldRef` of the field node to
                optionalise.
            namespace (str, optional): Can be omitted if previously
                set when initializing the client.
        """
        return self.set_optional(field, optional=True, namespace=namespace)

    @scoped("namespace")
    def unoptionalise(self, field, namespace=None):
        """Make a field node required (not optional)

        Exactly the same as `OverrideClient.set_optional(field,
        optional=False)`.

        Args:
            field (str): the `FieldRef` of the field node to
                unoptionalise.
            namespace (str, optional): Can be omitted if previously
                set when initializing the client.

        """
        return self.set_optional(field, optional=False, namespace=namespace)
