import random

from redag.entity.entity import entity_decorator, get_entity_references
from redag.entity.redag_types import EntityTypeEnum
from redag.redag import REDAG


def dimension(max_quantity=1):
    def f(cls):
        entity_decorator(EntityTypeEnum.DIMENSION)(cls)

        if Dimension not in cls.__bases__:
            raise ValueError("Dimension should derive from Dimension class!")
        if get_entity_references(cls):
            raise ValueError("Dimension entity can not have any references!")

        cls.max_dim_quantity = max_quantity
        REDAG().register_entity(cls)
        return cls

    return f


class DimensionMetaClass(type):
    """
    Restricts number of instances of a class to cls.max_dim_quantity.
    """
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
