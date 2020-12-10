import logging

from .client import Synth
from .model import (
    Array,
    Field,
    Object,
    OneOf,
    Faker,
    DateTime,
    Categorical,
    Bool,
    Number,
    SameAs,
    String,
)

from .exceptions import SynthException, ImproperlyConfigured, TransportError

logger = logging.getLogger("synthpy")
logger.addHandler(logging.NullHandler())

try:
    import pkg_resources
    __version__ = pkg_resources.require("getsynthpy")[0].version
except ImportError or pkg_resources.DistributionNotFound:
    __version__ = "unknown"


__all__ = [
    "Synth",
    "SynthException",
    "ImproperlyConfigured",
    "TransportError",
    "Array",
    "Field",
    "Object",
    "Faker",
    "OneOf",
    "DateTime",
    "Categorical",
    "Bool",
    "Number",
    "SameAs",
    "String",
    "__version__",
]
