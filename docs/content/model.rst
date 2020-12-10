.. _model:

Data Model API
==============
The ``Synth`` data model is a composable extension of the JSON data
model. It consists of the following familiar types:


- :class:`~synthpy.model.Object`: corresponds to a JSON object, i.e. a
  key/value store with string keys.
- :class:`~synthpy.model.Array`: correponds to a JSON array. They can
  be dynamically sized and a single array can host elements of many
  different types.
- :class:`~synthpy.model.String`: corresponds to a JSON string.
- :class:`~synthpy.model.Bool`: corresponds to a JSON boolean (``true``/``false``).
- :class:`~synthpy.model.Number`: corresponds to a JSON
  number. Numbers can be of any of three primitive types:

  - ``u64``: a 64 bit unsigned integer,
  - ``i64``: a 64 bit signed integer and
  - ``f64``: a 64 bit floating point number.

Together with the above, ``Synth`` introduces additional `logical`
types to specify custom logic binding the synthetic data model.

- :class:`~synthpy.model.OneOf`: an enumeration or union
  type. ``OneOf``'s regroup fixed collections of types. When sampling
  from those types, one of the variant is picked at random and is used
  to produce the generated value of the ``OneOf``. The probability of
  picking the different variants is inferred from training on real
  data, but can also be :doc:`overridden<./override>`.
- :class:`~synthpy.model.SameAs`: a reference or pointer
  type. ``SameAs``'s are pointers to other types. They allow for
  specifying that certain fields or elements must be the same at
  different places in any sample.

.. currentmodule:: synthpy.model

.. autosummary::
   :toctree: api/model

   Object
   Array
   String
   Bool
   Number
   OneOf
   SameAs
   Faker
   DateTime
   Categorical
