.. _namespace:

Namespace API
=============

``synthd``'s data model works with three concepts.

1. **Documents**: a `document` is simply a JSON object, i.e. a
   key-value store with string keys.
2. **Collections**: a `collection` is an array of `documents`.
3. **Namespaces**: a `namespace` is a key-value store of
   `collections`, with string keys.

The **Namespace API** is the subset of API functionalities of the
``synthd`` API that allows for listing namespaces, accessing their
inner data models' schemas and rollback operations.

.. currentmodule:: synthpy.client.namespace

.. autosummary::
   :toctree: api/namespace

   NamespaceClient
   NamespaceClient.delete_collection
   NamespaceClient.delete_namespace
   NamespaceClient.get_namespaces
   NamespaceClient.get_schema
   NamespaceClient.rollback_namespace
