import random
import string
from functools import singledispatch
from typing import List, Dict, Union, Callable

from generator import Generator

__GENERATOR_CONFIG_KEY__ = "__generator_config__"
__ENTITY_ATTRIBUTES_KEY__ = "__entity_attributes__"
__GENERATOR_KEY__ = "__generator_function__"

__TYPE_TO_DEFAULT_GENERATOR__ = {
    int: lambda *args, **kwargs: random.randint(0, 10),
    float: lambda *args, **kwargs: random.random(),
    str: lambda *args, **kwargs: ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
}


def entity(items: int):
    def f(cls):
        attr_to_type = __extract_attributes(cls)
        setattr(cls, __ENTITY_ATTRIBUTES_KEY__, attr_to_type)
        __create__init(cls)
        gen = __create_generator_function(__create_attr_generators(cls), attr_order=list(attr_to_type.keys()))
        setattr(cls, __GENERATOR_KEY__, gen)
        return cls

    return f


def generator(**kwargs):
    """
        Decorator used to declare entity methods as generators.

        Generator will be saved as classmethod in class __dict__.
        Dict of the classmethod will contain 2__GENERATOR_CONFIG__KEY__ with Generator object.
    """
    # If the name is not provided we treat it as all attributes generator
    name = kwargs.get("name", None)

    def dec(f: Callable) -> classmethod:
        f_cls = f if isinstance(f, classmethod) else classmethod(f)
        setattr(
            f_cls,
            __GENERATOR_CONFIG_KEY__,
            Generator(attr_name=name, func=f_cls.__func__)
        )
        return f_cls

    return dec


def __set_generator_function(cls, gen: Callable):
    setattr(cls, __GENERATOR_KEY__, gen)


def __extract_attributes(cls) -> Dict[str, type]:
    """
        Scan __annotation__ of class @cls to retrieve attributes together with their types.
    """
    return dict([(ann, value) for ann, value in cls.__dict__["__annotations__"].items() if not ann.startswith('_')])


def __extract_custom_generators(cls) -> List[Generator]:
    """
        Extract list of custom generators defined by the user for entity.
    """
    return [cls.__dict__[f].__dict__[__GENERATOR_CONFIG_KEY__] for f in cls.__dict__.keys()
            if isinstance(cls.__dict__[f], classmethod) and __GENERATOR_CONFIG_KEY__ in cls.__dict__[f].__dict__.keys()]


def __create_attr_generators(cls) -> Union[Dict[str, Generator], Generator]:
    """
        Create generator for each attribute of entity @cls.
    """
    custom_gens = __extract_custom_generators(cls)

    if any([g.attr_name is None for g in custom_gens]):
        if len(custom_gens) > 1:
            raise ValueError(f"Entity {cls.__name__} defined with more than one batch generator!")
        return custom_gens[0]

    attr_to_gen = dict([(g.attr_name, g) for g in custom_gens])

    for attr, type in cls.__dict__[__ENTITY_ATTRIBUTES_KEY__].items():
        if attr not in attr_to_gen:
            attr_to_gen[attr] = Generator(attr, __TYPE_TO_DEFAULT_GENERATOR__[type])

    return attr_to_gen


@singledispatch
def __create_generator_function(generators: dict[str, Generator], attr_order: List[str]):
    def __generator(cls):
        values = {}
        for a in attr_order:
            values[a] = generators[a].func(cls, values)
        return cls(**values)

    return classmethod(__generator)


@__create_generator_function.register
def _(generator: Generator, attr_order: List[str]):
    def __generator(cls):
        return cls(**generator.func(cls))

    return classmethod(__generator)


def __create__init(cls):
    attributes = list(cls.__dict__[__ENTITY_ATTRIBUTES_KEY__].keys())

    def __init__template(self, **kwargs):
        for attr in attributes:
            setattr(self, attr, kwargs[attr])

    setattr(cls, "__init__", __init__template)
