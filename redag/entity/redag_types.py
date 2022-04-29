import datetime
import random
import string
import time
import types
import uuid
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Any

Entity = type
EntityValue = Any


class EntityTypeEnum(Enum):
    FACT = auto()
    DIMENSION = auto()


@dataclass
class ObjectID:
    """
    Internal ID assigned to every instance of REDAG entity.
    """
    id: str

    @classmethod
    def generate(cls):
        return cls(id=str(uuid.uuid4()))

    def __str__(self):
        return self.id


@dataclass
class EntityGenerator:
    func: Callable


class ReferenceMetaClass(type):
    """
        Together with Reference class enables definition of
        generic references:
        Reference[Type]

        The Type parameter is persisted in @referenced_type key.
    """

    def __getitem__(cls, key):
        new_cls = types.new_class(f"{cls.__name__}_{key.__name__}", (cls,), {},
                                  lambda ns: ns.__setitem__("referenced_type", key))
        return new_cls


class Reference(metaclass=ReferenceMetaClass):
    referenced_id: ObjectID

    def __init__(self, referenced_id: ObjectID):
        self.referenced_id = referenced_id


def is_allowed_entity_attribute_types(t) -> bool:
    return t in [int, float, str, datetime.date, ObjectID, bool] or type(t) == ReferenceMetaClass


TYPE_TO_DEFAULT_GENERATOR = {
    int: lambda *args, **kwargs: random.randint(0, 10),
    float: lambda *args, **kwargs: random.random(),
    bool: lambda *args, **kwargs: bool(random.getrandbits(1)),
    str: lambda *args, **kwargs: ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
    datetime.date: lambda *args, **kwargs: datetime.datetime.fromtimestamp(
        int(time.time()) + 86400 * random.randint(0, 60))
}
