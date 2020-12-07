import logging

from .client import Synth

from .exceptions import (
    SynthException,
    ImproperlyConfigured,
    TransportError
)

logger = logging.getLogger("synthpy")
logger.addHandler(logging.NullHandler())

__all__ = [
    "Synth",
    "SynthException",
    "ImproperlyConfigured",
    "TransportError"
]
