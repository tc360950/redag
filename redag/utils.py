import uuid
from dataclasses import dataclass


@dataclass
class ObjectID:
    id: str

    @classmethod
    def generate(cls):
        return cls(id=str(uuid.uuid4()))