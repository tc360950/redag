from typing import Dict, Callable

from redag.entity.redag_annotations_processor import RedagAnnotationsProcessor as RAP
from redag.entity.redag_types import ObjectID, EntityGenerator, \
    ReferenceMetaClass, is_allowed_entity_attribute_types, TYPE_TO_DEFAULT_GENERATOR, Entity, EntityTypeEnum

__REDAG_ID_ATTRIBUTE__ = "__redag_id__"


def entity_decorator(entity_type: EntityTypeEnum):
    def f(cls: Entity):
        RAP.init_entity_redag_config(cls, entity_type)
        entity_attributes: Dict[str, type] = extract_entity_attributes(cls)
        RAP.set_entity_attributes(cls, entity_attributes)
        RAP.set_entity_init(cls, create_entity_init(cls))
        RAP.set_entity_generator(cls, create_generator_function(cls))

        if not all([RAP.is_redag_entity(r.referenced_type) for r in get_entity_references(cls).values()]):
            raise ValueError("You can only reference other entities!")
        return cls

    return f


def generator_decorator():
    """
        Decorator used to declare entity methods as generators.
    """

    def dec(f: Callable) -> classmethod:
        f_cls = f if isinstance(f, classmethod) else classmethod(f)
        RAP.set_generator_config_on_classmethod(f_cls, EntityGenerator(func=f_cls.__func__))
        return f_cls

    return dec


def multiplicity_generator_decorator():
    def dec(f: Callable) -> classmethod:
        f_cls = f if isinstance(f, classmethod) else classmethod(f)
        RAP.mark_classmethod_as_multiplicity_generator(f_cls)
        return f_cls

    return dec


def extract_entity_attributes(cls) -> Dict[str, type]:
    """
        Scan __annotation__ of class @cls to retrieve attributes together with their types.
    """
    attributes = dict(
        [(ann, value) for ann, value in cls.__dict__["__annotations__"].items()])

    # Always add ....
    attributes[__REDAG_ID_ATTRIBUTE__] = ObjectID

    if not all([is_allowed_entity_attribute_types(t) for t in attributes.values()]):
        raise ValueError(f"Class {cls.__name__} contains forbidden type!")

    return attributes


def create_entity_init(cls) -> Callable:
    """
        Each entity gets an 'all-attributes' constructor with exception of
        Redag's internal objectID - this one is generated automatically in the constructor.
    """
    attributes = list(RAP.get_entity_attributes(cls).keys())

    def __init__template(self, **kwargs):
        for attr in attributes:
            if attr != __REDAG_ID_ATTRIBUTE__:
                setattr(self, attr, kwargs[attr])
            else:
                setattr(self, __REDAG_ID_ATTRIBUTE__, ObjectID.generate())

    return __init__template


def create_generator_function(cls):
    """
    Create a proper generating function from method decorated with 'generator_decorator'
    (if none method has been indicated as generator, use default)
    """
    generator = RAP.get_entity_custom_generator_def(cls)
    if generator is None:
        generator = create_default_generator(cls)

    def __generator(cls, parents: Dict, state: Dict, **kwargs):
        # this call should result in generation of all attributes with exception of references
        attr_dict = generator.func(cls, parents=parents, state=state)
        for ref_name, ref_type in get_entity_references(cls).items():
            referenced_id = get_object_id(parents[ref_type.referenced_type])
            attr_dict[ref_name] = ref_type(referenced_id=referenced_id)
        return cls(**attr_dict)

    return classmethod(__generator)


def create_default_generator(cls) -> EntityGenerator:
    attributes = RAP.get_entity_attributes(cls)
    # Filter out references and id - those attributes will be generated internally
    attributes = dict([(name, type_) for name, type_ in attributes.items() if
                       type(type_) != ReferenceMetaClass and name != __REDAG_ID_ATTRIBUTE__])

    def __default_generator(cls, **kwargs):
        res = {}
        for attr, type_ in attributes.items():
            res[attr] = TYPE_TO_DEFAULT_GENERATOR[type_]()
        return res

    return EntityGenerator(func=__default_generator)


def get_entity_references(cls) -> Dict[str, type]:
    return {n: t for n, t in RAP.get_entity_attributes(cls).items() if type(t) == ReferenceMetaClass}


def get_object_id(object) -> ObjectID:
    if not RAP.is_redag_entity(type(object)):
        raise ValueError(f"Provided object {object} is not a Redag Entity!")
    return getattr(object, __REDAG_ID_ATTRIBUTE__)
