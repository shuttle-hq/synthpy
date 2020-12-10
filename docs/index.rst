.. synthpy documentation master file, created by
   sphinx-quickstart on Tue Nov 24 07:26:03 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. image:: images/getsynth_identicon.png
   :width: 300

**Date**: |today| **Version**: |release|

What is this?
~~~~~~~~~~~~~

This is `Synth <https://getsynth.com>`_! A fast and highly
configurable **NoSQL synthetic data engine**. It reconciles the two
worlds of `synthetic data
<https://en.wikipedia.org/wiki/Synthetic_data>`_ and `test data
<https://en.wikipedia.org/wiki/Test_data>`_ by letting users generate
realistic synthetic data for testing their applications and ML models.

What can I do with this?
~~~~~~~~~~~~~~~~~~~~~~~~

With ``Synth`` you can:

* **Anonymize sensitive data easily.**
   As simple as JSON-in/JSON-out. If you're not happy with the result,
   simply tweak the synthetic data model with a custom JSON metadata
   format and ``Synth`` will adjust everything on the fly, no
   additional ETL required.

* **Augment your datasets with synthetic data.**
   For those times when you already have some data but just not enough
   of it to do what you need to do. It can extrapolate from patterns
   it finds in your data, so you can create as much of it as you want.

* **Create entirely new fake data declaratively.**
   You can even add you own set of constraints and logic to create
   completely unseen scenario.


How does it work?
~~~~~~~~~~~~~~~~~

It has two components:

* :ref:`synthd<synthd>`: a persistent process that ingests raw (usually
  sensitive) training data and trains and builds synthetic data models
  from it. Think of it as a NoSQL datastore that never persists actual
  data, only anonymized model parameters.
* :ref:`synthpy <getting_started>`: a reference Python implementation for the
  :ref:`synthd<synthd>` API. This lets you leverage
  :ref:`synthd<synthd>` in custom scripts and test harnesses.

Quickstart
~~~~~~~~~~
Here is an end-to-end example using the Python client,
:ref:`synthpy <getting_started>`.

.. code-block:: python

   from synthpy import Synth

   # Assuming `synthd` is running on `localhost` with default settings
   client = Synth("localhost:8182")

   with open("my_users_data.json", "r") as data_f:
       documents = json.load(data_f)

   # Submit your JSON documents to `synthd` for training
   client.put_documents(namespace="app", collection="users", batch=documents)

   # Generate 100 new synthetic users
   synthetic_users = client.get_documents(namespace="app", collection="users", size=100)


In this guide
~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 2

   self
   content/installation
   content/getting_started
   content/core_concepts
   content/api

