.. _ingest:

Ingest API
==========
**Synth** relies on ingesting raw data samples in order to train its
internal model of your data. The **Ingest API** is a subset of API
functionalities of ``synthd`` that allows for ingesting data and thus,
training models from data.

.. currentmodule:: synthpy.client.ingest

.. autosummary::
   :toctree: api/ingest

   IngestClient
   IngestClient.put_documents
