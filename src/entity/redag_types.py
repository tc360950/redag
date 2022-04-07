import datetime
import random
import string
import types
import uuid
from dataclasses import dataclass
from typing import Callable


@dataclass
class ObjectID:
    id: str

    @classmethod
    def generate(cls):
        return cls(id=str(uuid.uuid4()))


@dataclass
class EntityGenerator:
    func: Callable


class ReferenceMetaClass(type):
    def __getitem__(cls, key):
        new_cls = types.new_class(f"{cls.__name__}_{key.__name__}", (cls,), {},
                                  lambda ns: ns.__setitem__("referenced_type", key))
        return new_cls


class Reference(metaclass=ReferenceMetaClass):
    referenced_id: ObjectID

    def __init__(self, referenced_id: ObjectID):
        self.referenced_id = referenced_id


def is_allowed_entity_attribute_types(t) -> bool:
    return t in [int, float, str, datetime.date, ObjectID] or type(t) == ReferenceMetaClass


TYPE_TO_DEFAULT_GENERATOR = {
    int: lambda *args, **kwargs: random.randint(0, 10),
    float: lambda *args, **kwargs: random.random(),
    str: lambda *args, **kwargs: ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
    datetime.date: lambda *args, **kwargs: "dupa"
}
