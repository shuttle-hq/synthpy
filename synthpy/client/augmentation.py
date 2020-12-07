from .transport import Method
from .utils import NamespacedClient


class AugmentationClient(NamespacedClient):
    """Base class for the Augmentation API."""

    def put_augmentation(self, namespace, field, augmentation):
        request = self.transport.request(Method.PUT)

        request.path.push(namespace).push("_augment")

        request.body(field=field, augmentation=augmentation)

        return request.execute()

    def delete_augmentation(self, namespace, field):
        request = self.transport.request(Method.DELETE)

        request.path.push(namespace).push("_augment")

        request.body(field=field)

        return request.execute()
