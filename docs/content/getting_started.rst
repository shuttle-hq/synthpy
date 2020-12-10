.. _getting_started:

``synthpy``
===========
.. note::
   This section assumes you have completed the :ref:`installation
   process <installation>` and have an instance of
   :ref:`synthd<synthd>` running on ``localhost:8182``. If your setup
   is different, you might need to make the appropriate changes to the
   examples given.

Install using pip
~~~~~~~~~~~~~~~~~
The recommended way to setup the client is using `pip
<https://pypi.org/project/pip/>`_. Simply run

.. code-block:: bash

   $ pip install getsynthpy

This will install the latest stable release of :ref:`synthpy <getting_started>`.

Install from source
~~~~~~~~~~~~~~~~~~~
Alternatively, you can install :ref:`synthpy <getting_started>` directly from
its source code hosted on `GitHub
<https://github.com/openquery-io/synthpy>`_.

.. code-block:: bash

   $ git clone https://github.com/openquery-io/synthpy.git
   $ cd synthpy/
   $ pip install -e .

Install with Nix Flakes
~~~~~~~~~~~~~~~~~~~~~~~
If you are using the `Nix <https://nixos.org/>`_ package manager, you
can also install :ref:`synthpy <getting_started>` using `Flakes
<https://nixos.wiki/wiki/Flakes>`_.

.. code-block:: bash

   $ TODO


Getting started
~~~~~~~~~~~~~~~
Once you have successfully installed :ref:`synthpy <getting_started>`, we can
get started generating some synthetic data. The first thing we have to
do is instantiate the main API client :class:`~synthpy.client.Synth`,
from which we can access all the functionalities of
:ref:`synthd<synthd>`. From a Python REPL:

.. code-block:: python

   >>> from synthpy import Synth
   >>> synth = Synth("localhost:8182")
   >>> synth.get_namespaces()  # to check everything is working as expected
   {}


Using the pre-configured interactive shell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`synthpy <getting_started>` ships a pre-configured interactive shell. It
can start either a standard Python REPL or an `IPython
<https://ipython.org/>`_ prompt. It gets started by the `synthpy
<https://github.com/openquery-io/synthpy/blob/master/bin/synthpy>`_
script. If you have installed :ref:`synthpy <getting_started>` as pointed to
above (and the script is in your ``PATH``), you can run it with:

.. code-block:: bash

   $ synthpy --host=localhost:8182

If you want to run the shell inside `IPython <https://ipython.org/>`_,
add the ``--ipython`` flag. You can also set a default namespace with
``--namespace``. For a full list of available arguments, run ``synthpy
--help``.

Once inside the shell, the client is available under the variable
``synth``.

.. code-block:: ipython

   In [1]: synth    
   Out[1]: <synthpy.client.Synth at 0x7fbb6f203150>

Most of the required classes have also been imported on startup for
convenience.
