from ..model import Deserializer


def scoped(*scope):
    def make_namespaced(f):
        def as_namespaced(self, *args, **kwargs):
            for key in scope:
                if key not in kwargs:
                    if key not in self.transport.defaults:
                        raise ValueError(
                            f"'{key}' is a required argument but it was not explicitly specified nor was it specified on initialization of the client. Try calling this method again with the '{key}' argument."
                        )
                    kwargs[key] = self.transport.get_default(key)
            ret = f(self, *args, **kwargs)
            return ret

        try:
            as_namespaced.__doc__ = f.__doc__
        except AttributeError:
            pass

        return as_namespaced

    return make_namespaced


def canonicalize(from_):
    if isinstance(from_, dict):
        out = {}
        for k, v in from_.items():
            v_ = canonicalize(v)
            if v_ is not None:
                out[k] = v_
        return out
    elif isinstance(from_, list):
        out = []
        for v in from_:
            v_ = canonicalize(v)
            if v_ is not None:
                out.append(v_)
        return out
    else:
        return from_


class NamespacedClient:
    """Base class for a section of the ``synthd`` client API.

    Individual APIs should inherit from ``NamespacedClient`` to
    interop easily with the root user-facing client object ``Synth``.
    """

    def __init__(self, client):
        self.client = client
        self.deserializer = Deserializer()

    @property
    def transport(self):
        return self.client.transport
