from typing import List

from src.entity.entity import entity_decorator, EntityTypeEnum, Entity, get_entity_references
from src.entity.redag_annotations_processor import RedagAnnotationsProcessor
from src.redag import REDAG


def fact():
    def f(cls):
        entity_decorator(EntityTypeEnum.FACT)(cls)

        if len(__get_fact_references(cls)) > 1:
            raise ValueError("Entities may have at most one reference to facts!")

        REDAG().register_entity(cls)
        return cls

    return f


def __get_fact_references(fact: Entity) -> List[Entity]:
    return [f for f in get_entity_references(fact).values() if RedagAnnotationsProcessor.get_entity_type(f.referenced_type) == EntityTypeEnum.FACT]