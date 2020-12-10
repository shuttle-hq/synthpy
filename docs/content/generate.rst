.. _generate:

Generate API
============

**Synth** is a synthetic data engine. It allows you to synthesize any
kind of semi-structured data - encoded as JSON. This removes sensitive
information from data that contains personal identifiers or other form
of confidential attributes. But **Synth** does it in a such a way that
the synthetic documents retain the original's distribution and their
statistical properties.

The ``Generate`` API is the key entrypoint to generating samples of
synthetic data.

.. currentmodule:: synthpy.client.generate

.. autosummary::
   :toctree: api/generate

   GenerateClient
   GenerateClient.get_documents
