import uuid
from dataclasses import dataclass


@dataclass
class ObjectID:
    id: str

    @classmethod
    def generate(cls):
        return cls(id=str(uuid.uuid4()))


def get_type(obj) -> type:
    if type(obj) == type:
        return obj
    return type(obj)