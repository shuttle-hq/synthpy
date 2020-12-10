<p>
  <img width=30% src="https://github.com/openquery-io/synthpy/raw/master/docs/images/getsynth_identicon.png">
</p>

* License: [Apache v2.0](LICENSE)
* Documentation: https://openquery-io.github.io/synthpy/
* Homepage: https://getsynth.com

# What is this?

This is [`Synth`][getsynth]! A fast and highly
configurable **NoSQL synthetic data engine**. It reconciles the two
worlds of [**synthetic data**](https://en.wikipedia.org/wiki/Synthetic_data) and [**test data**](https://en.wikipedia.org/wiki/Test_data) by letting users generate
realistic synthetic data for testing their applications and ML models.

# What can I do with this?

With [`Synth`][getsynth] you can:

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
   
# How does it work?

It has two components:

* [`synthd`][synthd]: a persistent process that ingests raw (usually
  sensitive) training data and trains and builds synthetic data models
  from it. Think of it as a NoSQL datastore that never persists actual
  data, only anonymized model parameters.
* [`synthpy`][synthpy]: our reference Python implementation for the
  [`synthd`][synthd] API. This lets you leverage [`synthd`][synthd] in
  custom scripts and test harnesses.
  
# Quickstart

Here is an end-to-end example using the Python client, [`synthpy`][synthpy].

```python
from synthpy import Synth

# Assuming `synthd` is running on `localhost` with default settings
client = Synth("localhost:8182")

with open("my_users_data.json", "r") as data_f:
    documents = json.load(data_f)

# Submit your JSON documents to `synthd` for training
client.put_documents(namespace="app", collection="users", batch=documents)

# Generate 100 new synthetic users
synthetic_users = client.get_documents(namespace="app", collection="users", size=100)
```

# Want to know more?

As of now, only the Python client for [`Synth`][getsynth] is free and
open-source. But it is also on our roadmap to open-source big chunks
of the daemon, [`synthd`][synthd], where the real magic happens! So
stay tuned!

In the meantime, head over to our [documentation][docs] or hit us up
if you want to [give Synth a try][contact-us]!

[getsynth]: https://getsynth.com
[synthd]: https://github.com/openquery-io/synthpy/content/installation.html
[synthpy]: https://github.com/openquery-io/synthpy/content/getting_started.html
[docs]: https://openquery-io.github.io/synthpy/
[contact-us]: https://www.getsynth.com/contact
