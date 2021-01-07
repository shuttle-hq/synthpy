from ruamel.yaml import YAML
from io import StringIO


class Model:
    def __init__(self, type=None, **kwargs):
        self._kwargs = kwargs

        if type:
            self._type = type

    def _into_content(self):
        return self

    def __getitem__(self, idx):
        return self._kwargs[idx]

    def __setitem__(self, idx, what):
        self._kwargs[idx] = what

    def __delitem__(self, idx):
        del self._kwargs[idx]

    def __iter__(self):
        return iter(self._kwargs)

    def __str__(self):
        return YAMLSerializer().dumps(self)

    def _repr_pretty_(self, p, cycle):
        as_yaml = YAMLSerializer().dumps(self)
        p.text(as_yaml)

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_mapping(cls.yaml_tag, node._kwargs)

    def _into_repr(self):
        out = {}
        for k, v in self._kwargs.items():
            try:
                v = v._into_repr()
            except AttributeError:
                if isinstance(v, list):
                    v_ = []
                    for element in v:
                        try:
                            v_.append(element._into_repr())
                        except AttributeError:
                            v_.append(element)
                    v = v_
            out[k] = v

        try:
            out["type"] = self._type
        except AttributeError:
            pass

        return out


def number_subtype(instances):
    subtypes = []
    for instance in instances:
        if isinstance(instance, int):
            if instance >= 0:
                subtypes.append(0)
            else:
                subtypes.append(1)
        else:
            subtypes.append(2)

    max_ = max(subtypes)
    if max_ == 0:
        return "u64"
    elif max_ == 1:
        return "i64"
    elif max_ == 2:
        return "f64"


class YAMLSerializer:
    def __init__(self):
        yaml = YAML()

        for cls in [
            Array,
            OneOf,
            SameAs,
            Object,
            Number,
            String,
            Bool,
            DateTime,
            Faker,
            Range,
        ]:
            yaml.register_class(cls)

        self._yaml = yaml

    def _represent_untagged(self, representer, node):
        return representer.represent_mapping(node._kwargs)

    def dumps(self, model):
        buf = StringIO()
        self.dump(model, buf)
        return buf.getvalue()

    def dump(self, model, where):
        return self._yaml.dump(model, where)


class Deserializer:
    def __init__(self, ignore={"type"}):
        self.ignore = ignore

    def load(self, as_dict):
        try:
            type_ = as_dict.pop("type")
        except KeyError:
            type_ = "object"
        if type_ == "string":
            return self.unwrap_variant(String, as_dict)
        elif type_ == "number":
            subtype = as_dict.pop("subtype")
            return self.unwrap_variant(Number, as_dict, subtype=subtype)
        elif type_ == "bool":
            return self.unwrap_variant(Bool, as_dict)
        elif type_ == "same_as":
            return SameAs(as_dict["ref"])
        elif type_ == "array":
            length = self.load(as_dict.pop("length"))
            content = self.load(as_dict.pop("content"))
            return Array(content=content, length=length, **as_dict)
        elif type_ == "object":
            kwargs = {}
            for key in as_dict:
                try:
                    optional = as_dict[key].pop("optional")
                except KeyError:
                    optional = None
                kwargs[key] = self.load(as_dict[key])
                if optional is not None:
                    kwargs[key]._kwargs["optional"] = optional
            return Object(**kwargs)
        elif type_ == "one_of":
            variants = []
            for variant in as_dict["variants"]:
                weight = variant.pop("weight")
                variant_ = self.load(variant)
                variant_._kwargs["weight"] = weight
                variants.append(variant_)
            return OneOf(variants=variants)
        else:
            raise ValueError("unknown model type: '{}'", type_)

    async def load_coro(self, coro):
        as_dict = await coro
        return self.load(as_dict)

    def unwrap_variant(self, ty, content, **kwargs):
        variant_name = self.unwrap_exactly_one_key(content)
        variant_content = content[variant_name]
        if isinstance(variant_content, dict):
            return getattr(ty, variant_name)(**variant_content, **kwargs)
        else:
            return getattr(ty, variant_name)(variant_content, **kwargs)

    def unwrap_exactly_one_key(self, from_):
        keys = set(from_.keys())
        for ignored in self.ignore:
            if ignored in keys:
                keys.remove(ignored)

        if len(keys) != 1:
            raise ValueError(f"expected exactly one key, got {len(keys)}: {keys}")

        return keys.pop()


class Array(Model):
    """Model type for a JSON array

    Args:
        content (optional, Model): the content of this array. If
            specified, must be a model instance.
        length (optional, Model): the length of the generated
            array. If specified, must be a model generating
            non-negative numbers.
    """

    yaml_tag = "!array"

    def __init__(self, content=None, length=None):
        super(Array, self).__init__(type="array", content=content, length=length)


class Object(Model):
    """Model type for a JSON object

    Args:
        **kwargs: key/value pairs of fields in the object. Values must
            be model instances.
    """

    yaml_tag = "!object"

    def __init__(self, **kwargs):
        super(Object, self).__init__(type="object", **kwargs)

    def __iter__(self):
        return filter(lambda x: x != "type", super(Object, self).__iter__())


class Faker(Model):
    """A subtype for string models that generate values from a
    `faker provider <https://faker.readthedocs.io/en/master/providers.html>`_

    Args:
        generator (str, optional): the name of a faker attribute to
            sample from
        **kwargs (optional): additional arguments to pass to the
            underlying faker generator
    """

    yaml_tag = "!faker"

    def __init__(self, generator=None, **kwargs):
        super(Faker, self).__init__(generator=generator, **kwargs)

    def _into_content(self):
        return String(self)


class DateTime(Model):
    """A subtype for string models that generate values from a
    date/time/datetime range

    Args:
        format (str): the `string to format <https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior>`_ timestamps with
        type (str, optional): one of "naive_date", "naive_time",
            "naive_date_time" or "date_time".
        begin (str, optional): the lowest possible date/time.
        end (str, optional): the highest possible date/time.
    """

    yaml_tag = "!date_time"

    def __init__(self, format=None, subtype=None, begin=None, end=None):
        super(DateTime, self).__init__(
            format=format, subtype=subtype, begin=begin, end=end
        )

    def _into_content(self):
        return String(self)


class Categorical(Model):
    def __init__(self, choices):
        raise NotImplementedError

    def _into_content(self):
        raise NotImplementedError


class Bool(Model):
    """Model type for a JSON boolean

    The ``variant`` argument must be one of:

    - `float`: a `float` between ``0.`` and ``1.`` encoding the
      probability for the boolean to be ``True``.
    - `bool`: specifies that the ``Bool`` model is constant at the
      given value.
    - :class:`~synthpy.model.Categorical`: the specification of a
      categorical domain to sample from. Elements must be booleans.
    """

    yaml_tag = "!bool"

    def __init__(self, variant):
        kwargs = {}
        if isinstance(variant, bool):
            kwargs["constant"] = variant
        elif isinstance(variant, float):
            kwargs["frequency"] = variant
        elif isinstance(variant, Categorical):
            kwargs["categorical"] = variant
        else:
            raise ValueError("'variant' must be one of 'bool', 'float', 'Categorical'")
        super(Bool, self).__init__(type="bool", **kwargs)

    @classmethod
    def constant(cls, c):
        """Builds a ``Bool`` model generating only the given value.

        Same as ``Bool(c)``.

        Args:
            c (bool): a constant value
        """
        return cls(c)

    @classmethod
    def frequency(cls, f):
        """Builds a ``Bool`` model generating ``True`` at the given frequency.

        Same as ``Bool(f)``.

        Args:
            f (float, between 0. and 1.): the frequency at which
                ``True`` is sampled
        """
        return cls(f)

    @classmethod
    def categorical(cls, choices):
        return cls(choices)


class Number(Model):
    """Model type for a JSON number

    The ``variant`` argument must be one of:

    - ``range``: for a number model constrained in an interval
    - ``float/int``: for a number model yielding only constant values
    - ``Categorical``: a Categorical model

    Args:
        variant (optional): a variant of number model, as described
            above.
        subtype (str, optional): if specified, must be one of "f64",
            "i64", "u64".
    """

    yaml_tag = "!number"

    def __init__(self, variant, subtype=None):
        kwargs = {}
        if isinstance(variant, Range) or isinstance(variant, range):
            variant = Range._ensure(variant)
            inferred = number_subtype([variant.start, variant.stop])
            kwargs["range"] = variant
        elif isinstance(variant, Categorical):
            inferred = number_subtype(variant.choices)
            kwargs["categorical"] = variant
        elif isinstance(variant, int) or isinstance(variant, float):
            inferred = number_subtype([variant])
            kwargs["constant"] = variant
        kwargs["subtype"] = subtype or inferred
        super(Number, self).__init__(type="number", **kwargs)

    @classmethod
    def range(cls, *args, subtype=None, **kwargs):
        """Build a ``Number`` model from an interval"""
        if kwargs:
            assert len(args) == 0
            r = Range(kwargs["low"], kwargs["high"], kwargs["step"])
        else:
            [r] = args
            assert isinstance(r, Range) or isinstance(r, range)
        return cls(r, subtype=subtype)

    @classmethod
    def constant(cls, c, subtype=None):
        """Build a ``Number`` model generating only a constant number"""
        return cls(c, subtype=subtype)

    @classmethod
    def categorical(cls, choices, subtype=None):
        return cls(choices, subtype=subtype)


class Range(Model):
    yaml_tag = "!range"

    def __init__(self, low, high, step=None):
        super(Range, self).__init__(low=low, high=high, step=step)

    @classmethod
    def _ensure(cls, variant):
        if isinstance(variant, range):
            return Range(low=variant.start, high=variant.stop, step=variant.step)
        elif isinstance(variant, cls):
            return variant
        else:
            raise ValueError(
                f"do not know how to convert into 'Range' for {type(variant)}"
            )

    @property
    def start(self):
        return self["low"]

    @property
    def stop(self):
        return self["high"]

    @property
    def step(self):
        return self["step"]

    def _into_content(self):
        return Number(self)


class SameAs(Model):
    """Model type for a reference

    Args:
        ref (str): a field address that is the pointee of this
            reference.
    """

    yaml_tag = "!same_as"

    def __init__(self, ref):
        super(SameAs, self).__init__(type="same_as", ref=ref)


class OneOf(Model):
    """Model type for an enumeration of models

    A ``OneOf`` allows for specifying a model whose values are
    generated from a fixed collection of possible variants. For
    example, a model that is allowed to generate either strings or
    numbers would be specified as a ``OneOf``.

    Example:
       .. code-block:: python

          OneOf([String.pattern("[a-z]{1,9}"), Number.constant(2)])

    Args:
        variants (optional, List[Model]): the possible variants of
            this enumeration. If specified, must be a list of model
            instances.

    """

    yaml_tag = "!one_of"

    def __init__(self, variants):
        super(OneOf, self).__init__(type="one_of", variants=variants)

    def __len__(self):
        return len(self._kwargs["variants"])

    def __iter__(self):
        return iter(self._kwargs["variants"])


class String(Model):
    """Model type for a JSON string

    The ``variant`` argument must be one of:

    - `str`: a valid regex string to sample from
    - :class:`~synthpy.model.Faker`: the specification of a faker generator to sample from
    - :class:`~synthpy.model.DateTime`: the specification of a date/time/datetime range to sample from
    - :class:`~synthpy.model.Categorical`: the specification of a
      categorical domain to sample from. Elements must be strings.

    Args:
        variant (optional): a variant of string model, as described
            above.
    """

    yaml_tag = "!string"

    def __init__(self, variant):
        kwargs = {}
        if isinstance(variant, Faker):
            kwargs["faker"] = variant
        elif isinstance(variant, str):
            kwargs["pattern"] = variant
        elif isinstance(variant, DateTime):
            kwargs["date_time"] = variant
        elif isinstance(variant, Categorical):
            kwargs["categorical"] = variant
        else:
            raise ValueError(
                "'variant' must be one of 'Faker', 'str', 'DateTime', 'Categorical'"
            )
        super(String, self).__init__(type="string", **kwargs)

    @classmethod
    def faker(cls, generator=None, **kwargs):
        """Build a ``String`` model generating strings from a faker provider.

        Arguments are the same as for :class:`~synthpy.model.Faker`.
        """
        return Faker(generator=generator, **kwargs)._into_content()

    @classmethod
    def pattern(cls, regex=None):
        """Build a ``String`` model generating only strings that validate for
        a given regex.

        Args:
            regex (str, optional): a valid regex
        """
        return cls(regex)

    @classmethod
    def date_time(cls, format=None, subtype=None, begin=None, end=None):
        """Build a ``String`` model generating valid ``strftime``
        formatted dates, times and datetimes.

        Arguments are the same as for :class:`~synthpy.model.DateTime`.
        """
        return DateTime(
            format=format, subtype=subtype, begin=begin, end=end
        )._into_content()

    @classmethod
    def categorical(cls, choices):
        raise NotImplementedError

    def _into_content(self):
        return self
