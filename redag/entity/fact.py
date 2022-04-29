from typing import List

from redag.entity.entity import entity_decorator, EntityTypeEnum, Entity, get_entity_references
from redag.entity.redag_annotations_processor import RedagAnnotationsProcessor as RAP
from redag.redag import REDAG


def fact():
    def f(cls):
        entity_decorator(EntityTypeEnum.FACT)(cls)

        if len(__get_fact_references(cls)) > 1:
            raise ValueError("Entities may have at most one reference to facts!")

        REDAG().register_entity(cls)
        return cls

    return f


def __get_fact_references(fact: Entity) -> List[Entity]:
    return [f for f in get_entity_references(fact).values() if RAP.get_entity_type(f.referenced_type) == EntityTypeEnum.FACT]