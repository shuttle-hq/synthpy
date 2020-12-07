.. synthpy documentation master file, created by
   sphinx-quickstart on Tue Nov 24 07:26:03 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Synth: The NoSQL Synthetic Data Engine
======================================

**Synth** is a fast and versatile NoSQL synthetic data engine for
semi-structured data.

What can I do with this?
~~~~~~~~~~~~~~~~~~~~~~~~

With **Synth** you can:

* **Anonymize** sensitive data for use in the development and testing of
  applications and machine learning models.
* **Augment** your existing data with look-alike synthetic data to help you
  develop your application at scale.
* **Create** new fake or dummy data with user-specified sets of
  constraints, bounds and relations.

Overview
~~~~~~~~

**Synth** is comprised of two components:

* :ref:`synthd`: the persistent process that manages synthetic data models.
* Client implementations: bindings for the :ref:`synthd` API in
  various languages.

Getting started
~~~~~~~~~~~~~~~
Here is a simple end-to-end example in `Python`. **outdated!**

.. code-block:: python

   from datetime import datetime
   from synthpy import Synth

   # Assuming `synthd` is running on `localhost` with default settings
   client = Synth("localhost:8182")

   document = {
       "username": "totally_real_user_1337",
       "email": "tru_1337@gmail.com",
       "created_at": datetime.now(),
       "num_logins": 16
   }

   client.ingest.put_documents("my_namespace", "users", document=document)

   synthetic_user = client.generate.get_documents("my_namespace", "users", size=1)


Going in deep
~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 2

   content/synthd
   content/synthpy

