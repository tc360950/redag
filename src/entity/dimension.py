import random

from src.entity.entity import entity_decorator, EntityTypeEnum, get_entity_references
from src.redag import Redag


def dimension(max_quantity=1):
    def f(cls):
        entity_decorator(EntityTypeEnum.DIMENSION)(cls)

        if Dimension not in cls.__bases__:
            raise ValueError("Dimension should derive from Dimension class!")
        if get_entity_references(cls):
            raise ValueError("Dimension entity can not have any references!")

        cls.max_dim_quantity = max_quantity
        Redag().register_entity(cls)
        return cls

    return f


class DimensionMetaClass(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        number_of_instances = len(DimensionMetaClass.instances.get(cls, []))
        index = random.randint(0, cls.max_dim_quantity - 1)
        if index < number_of_instances:
            return DimensionMetaClass.instances[cls][index]
        else:
            new_instance = super(DimensionMetaClass, cls).__call__(*args, **kwargs)
            DimensionMetaClass.instances.setdefault(cls, []).append(new_instance)
            return new_instance


class Dimension(metaclass=DimensionMetaClass):
    pass
