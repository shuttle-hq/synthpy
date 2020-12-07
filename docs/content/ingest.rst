.. _ingest:

Ingest
======
**Synth** relies on ingesting raw data samples in order to train its
internal model of your data.

The ``Ingest`` API is the key entrypoint to uploading raw data to ``synthd``.

.. currentmodule:: synthpy.client.ingest

.. autosummary::
   :toctree: api/ingest

   IngestClient
   IngestClient.put_documents
