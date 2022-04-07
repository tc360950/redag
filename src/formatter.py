from typing import List, Dict, Any

from src.entity.entity import Entity
from src.entity.redag_annotations_processor import RedagAnnotationsProcessor
from src.entity.redag_types import ObjectID, ReferenceMetaClass
from src.redag import Redag


class RedagSampleFormatter:

    @staticmethod
    def format(sample: Redag.Sample) -> List[Dict[str, Any]]:
        result = []
        for t, e in sample.entities.items():
            for ee in e:
                result.append(RedagSampleFormatter.__format_entity(t, ee))

        return result

    @staticmethod
    def __format_entity(entity: Entity, value: Any) -> Dict[str, Any]:
        attributes = RedagAnnotationsProcessor.get_entity_attributes(entity)
        entity_dict = {"entity": entity.__name__}
        for attr, attr_type in RedagAnnotationsProcessor.get_entity_attributes(entity).items():
            if attr_type == ObjectID:
                entity_dict["id"] = value.__getattribute__(attr).id
            elif type(attr_type) == ReferenceMetaClass:
                continue
            else:
                entity_dict[attr] = value.__getattribute__(attr)

        return entity_dict