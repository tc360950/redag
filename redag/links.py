from dataclasses import dataclass


@dataclass
class Reference:
    entity: type


class EntityReference(Reference):
    pass


class OneToManyReference(Reference):
    pass
