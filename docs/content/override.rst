.. _override:

Override API
============
**Synth** builds statistical models of data automagically from
scanning real data. That great strength is sometimes also a weakness
and it is important to be able to manually specify additional
constraints and custom high-level logic on top of the
statistically-inferred information.

The **Override API** is the subset of API functionalities of ``synthd``
that allows for overriding statistically-inferred data
models. Effectively, it lets you specify the bounding box in which the
core ML-driven data model can freely train. This includes specifying
one-to-one, one-to-many, many-to-one relations between collections;
date time formats; custom string generators; etc.

For more on how :ref:`synthd <synthd>` handles overrides, see
:ref:`Overrides <overrides>`.

.. currentmodule:: synthpy.client.override

.. autosummary::
   :toctree: api/override

   OverrideClient
   OverrideClient.put_override
   OverrideClient.delete_override
   OverrideClient.set_optional
   OverrideClient.optionalise
   OverrideClient.unoptionalise
