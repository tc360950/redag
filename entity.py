import random
import string
from functools import singledispatch
from typing import List, Dict, Union

from generator import Generator, __GENERATOR_CONFIG_KEY__

__ENTITY_ATTRIBUTES_KEY__ = "__entity_attributes__"

__TYPE_TO_DEFAULT_GENERATOR__ = {
    int: lambda _: random.randint(0, 10),
    float: lambda _: random.random(),
    str: lambda _: ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
}

__GENERATOR_KEY__ = "__generator_function__"


def entity(items=100):
    print(items)

    def f(cls):
        ordered_attributes = __extract_attributes(cls)
        print(ordered_attributes)
        __create__init(cls)
        setattr(cls, __GENERATOR_KEY__, __create_generator_function(__extract_generators(cls.__dict__), ordered_attributes))
        return cls

    return f


def __extract_attributes(cls) -> List[str]:
    attributes = {}
    ordered_attr = []
    for ann, value in cls.__dict__["__annotations__"].items():
        if not ann.startswith('_'):
            attributes[ann] = value
            ordered_attr.append(ann)
    setattr(cls, __ENTITY_ATTRIBUTES_KEY__, attributes)
    return ordered_attr


# Get custom generators defined by the user
def __extract_custom_generators(class_dict: Dict) -> List[Generator]:
    return [class_dict[f].__dict__[__GENERATOR_CONFIG_KEY__] for f in class_dict.keys()
            if isinstance(class_dict[f], classmethod) and __GENERATOR_CONFIG_KEY__ in class_dict[f].__dict__.keys()]


def __extract_generators(class_dict: Dict) -> Union[Dict[str, Generator], Generator]:
    generators = __extract_custom_generators(class_dict)

    if any([g.attr_name is None for g in generators]):
        print(f"Batch generator defined for class...")
        return next(iter([g for g in generators if g.attr_name is None]), None)

    attribute_to_generator = dict([(g.attr_name, g) for g in generators])
    for attr, type in class_dict[__ENTITY_ATTRIBUTES_KEY__].items():
        if attr not in attribute_to_generator:
            attribute_to_generator[attr] = __TYPE_TO_DEFAULT_GENERATOR__[type]

    return attribute_to_generator


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
