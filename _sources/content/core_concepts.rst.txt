.. _Postman: https://documenter.getpostman.com/view/8887939/TVmS9GDG
.. _core_concepts:

Core Concepts
=============

.. warning::

   This page is WIP! In the meantime, you can use our `Postman`_ documentation.

What is ``synthd``?
~~~~~~~~~~~~~~~~~~~
:ref:`synthd<synthd>` is the `Synth <https://getsynth.com>`_
daemon. It is a persistent process that manages and serves synthetic
data models. `Synth <https://getsynth.com>`_ uses different code for
the daemon and the client. The daemon exposes a *RESTful* API that can
be consumed either directly by your own tooling or through client
implementations.

The daemon is responsible for ingesting raw training data (usually
containing sensitive information and PII), training and persisting
models and generating synthetic data (free of PII).

Data model
~~~~~~~~~~
TODO

Ingestion
~~~~~~~~~
TODO

Inference
~~~~~~~~~
TODO

.. _overrides:

Overrides
~~~~~~~~~
TODO

Data privacy
~~~~~~~~~~~~
TODO 
