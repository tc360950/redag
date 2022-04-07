from typing import Dict, Callable, Optional

from src.entity.entity_type import EntityTypeEnum
from src.entity.redag_types import EntityGenerator


class RedagAnnotationsProcessor:
    __REDAG_KEY__ = "__REDAG_KEY__"
    __ENTITY_ATTRIBUTES_KEY__ = "__entity_attributes__"
    __GENERATOR_KEY__ = "__generator_function__"
    __GENERATOR_CONFIG_KEY__ = "__generator_config__"
    __MULTIPLICITY_GENERATOR_KEY__ = "multiplicity"
    __ENTITY_TYPE_KEY__ = "entoty_type"

    @staticmethod
    def init_entity_redag_config(cls, entity_type: EntityTypeEnum) -> None:
        setattr(cls, RedagAnnotationsProcessor.__REDAG_KEY__, {})
        getattr(cls, RedagAnnotationsProcessor.__REDAG_KEY__)[RedagAnnotationsProcessor.__ENTITY_TYPE_KEY__] = entity_type

    @staticmethod
    def is_redag_entity(cls) -> bool:
        return hasattr(cls, RedagAnnotationsProcessor.__REDAG_KEY__)

    @staticmethod
    def get_entity_type(cls) -> EntityTypeEnum:
        return getattr(cls, RedagAnnotationsProcessor.__REDAG_KEY__)[RedagAnnotationsProcessor.__ENTITY_TYPE_KEY__]

    @staticmethod
    def set_entity_attributes(cls, attributes: Dict[str, type]) -> None:
        getattr(cls, RedagAnnotationsProcessor.__REDAG_KEY__)[
            RedagAnnotationsProcessor.__ENTITY_ATTRIBUTES_KEY__] = attributes

    @staticmethod
    def set_entity_generator(cls, generator: classmethod) -> None:
        getattr(cls, RedagAnnotationsProcessor.__REDAG_KEY__)[
            RedagAnnotationsProcessor.__GENERATOR_KEY__] = generator

    @staticmethod
    def get_entity_generator(cls) -> classmethod:
        return getattr(cls, RedagAnnotationsProcessor.__REDAG_KEY__)[
            RedagAnnotationsProcessor.__GENERATOR_KEY__]

    @staticmethod
    def get_entity_attributes(cls) -> Dict[str, type]:
        return getattr(cls, RedagAnnotationsProcessor.__REDAG_KEY__)[
            RedagAnnotationsProcessor.__ENTITY_ATTRIBUTES_KEY__]

    @staticmethod
    def set_entity_init(cls, init: Callable) -> None:
        setattr(cls, "__init__", init)

    @staticmethod
    def get_entity_custom_generator_def(cls) -> Optional[EntityGenerator]:
        return next(iter([
            cls.__dict__[f].__dict__[RedagAnnotationsProcessor.__GENERATOR_CONFIG_KEY__]
            for f in cls.__dict__.keys()
            if isinstance(cls.__dict__[f], classmethod)
               and RedagAnnotationsProcessor.__GENERATOR_CONFIG_KEY__ in cls.__dict__[f].__dict__.keys()
        ]), None)

    @staticmethod
    def set_generator_config_on_classmethod(cf: classmethod, gen: EntityGenerator) -> None:
        setattr(
            cf,
            RedagAnnotationsProcessor.__GENERATOR_CONFIG_KEY__,
            gen
        )

    @staticmethod
    def mark_classmethod_as_multiplicity_generator(f_cls):
        setattr(
            f_cls,
            RedagAnnotationsProcessor.__MULTIPLICITY_GENERATOR_KEY__,
            True
        )

    @staticmethod
    def get_entity_multiplicity_generator(cls) -> Optional[classmethod]:
        def __dimension_multiplicity(*args, **kwargs):
            return 1

        if RedagAnnotationsProcessor.get_entity_type(cls) == EntityTypeEnum.DIMENSION:
            return classmethod(__dimension_multiplicity)

        return next(iter([
            cls.__dict__[f]
            for f in cls.__dict__.keys()
            if isinstance(cls.__dict__[f], classmethod)
               and RedagAnnotationsProcessor.__MULTIPLICITY_GENERATOR_KEY__ in cls.__dict__[f].__dict__.keys()
        ]), classmethod(__dimension_multiplicity))