.. _installation:
.. _synthd:

Installation
============
.. note::
   To keep going, you will need to request IAM access to our release
   GCP project. If you are not already a customer and would like to
   see ``Synth`` in action, `let us know!
   <https://www.getsynth.com/contact>`_

Requirements
~~~~~~~~~~~~
To follow along with this guide, you'll have to have a valid `GCP
<https://cloud.google.com/>`_ account for you or your organization and
have the `Cloud SDK <https://cloud.google.com/sdk>`_ installed and
logged in on your machine. Depending on what installation track you
elect to follow, you will also need various IAM permissions to be
granted against our release GCP project.


First step
~~~~~~~~~~

First we need to setup :ref:`synthd<synthd>`. We have a couple
options:

1. Run it **standalone** from a bundled executable that ships all the
   runtime and libraries that :ref:`synthd<synthd>` uses. This is a
   good quick solution to get hacking locally but is less stable and
   does not have as good performance owing to its overheads.

2. Deploy our line-up of **custom VM images**. This is the preferred
   solution for use in production. Especially when working in an
   organization or any setup in which :ref:`synthd<synthd>` will be
   used by more than one user or on heavy datasets.

Standalone
~~~~~~~~~~
In standalone mode, you just need to drag and drop a single executable
binary in your environment. The binary includes an archive of all the
runtime and dependencies :ref:`synthd<synthd>` requires. This adds an
overhead and can significantly impact :ref:`synthd<synthd>`'s
performance, especially on start up.

The acquire the package, assuming you have been added to the relevant
`IAM permissions set
<https://cloud.google.com/storage/docs/access-control/iam-permissions>`_:

.. code-block:: bash

   $ gsutil cp gs://getsynth-enterprise/standalone/x86_64-linux/latest synthd
   $ chmod +x synthd
   $ ./synthd

We currently only have automated builds for ``Linux x86_64``. If
you need more OS/architecture configurations, let us know!

Deploying from VM images
~~~~~~~~~~~~~~~~~~~~~~~~
We maintain automated builds of `custom VM images
<https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images>`_
that can be used to provision VM instances running pre-configured
:ref:`synthd<synthd>`.

We recommend to get started with deploying a ``n2-standard-4``
`instance type <https://cloud.google.com/compute/docs/machine-types>`_
as a fair trade off between performance and cost for most starting use
cases. This can be changed later on if your needs turn out to be less
or more than expected. In addition, we recommend deploying the image
with at least ``200GiB`` of SSD persistent disk space and
**disabling** the `Delete boot disk when instance is deleted` option
to avoid losing trained data models.

To get started with custom images: follow the instructions `here
<https://cloud.google.com/compute/docs/images>`_ to make sure you
indeed have access to them. You will find them under the ``getsynth``
GCP project.

Atlernatively, from the console, run

.. code-block:: bash

   $ gcloud compute images list

Our image names follow a standard convention:
``synth-enterprise-${REV}-v${VERSION}``, where ``${REV}`` is the
originating ``git`` commit hash of the build and ``${VERSION}`` is the
day of the build encoded as ``"%Y%m%d"``. When deploying, it is
generally recommended to pick the latest build unless we have advised
you explictly otherwise.

Once you have established you have access to the images, follow the
instructions `here
<https://cloud.google.com/compute/docs/disks/create-root-persistent-disks#creatingrootpdalone>`_
to have them deployed in your VM infrastructure. Depending on your
setup, you might have to also setup firewall rules or ssh
port-forwarding in order to let the client on your local machine
access the daemon. By default, the daemon listens to HTTP requests
on ``0.0.0.0:8182``.

.. note::

   If you wish to use the guest tools's `OS Login
   <https://cloud.google.com/compute/docs/images/install-guest-environment>`_
   feature, you must create the instance with the additional metadata
   ``enable-oslogin=TRUE``.

Alternatively, you can deploy the image using ``Cloud SDK`` from the
command-line by running:

.. code-block:: bash

   $ gcloud compute instances create \
         --no-boot-disk-auto-delete \
         --boot-disk-size 200GiB \
         --boot-disk-type=pd-ssd \
         --machine-type n2-standard-4 \
         --image-project getsynth \
         --image synth-enterprise-${REV}-${VERSION} \
         --zone europe-west2-b \
	 --metadata=enable-oslogin=TRUE \
	 synth-enterprise-master

