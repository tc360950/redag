from typing import List, Dict, Any

from redag.entity.entity import Entity, get_entity_references, get_object_id
from redag.entity.redag_annotations_processor import RedagAnnotationsProcessor
from redag.entity.redag_types import ObjectID, ReferenceMetaClass, EntityValue
from redag.redag import REDAG


class SampleFormatter:
    """
        Transforms REDAG.Sample object into dictionaries (JSONs) which are easier to read and
        contain more redundant information.
    """
    @staticmethod
    def format(sample: REDAG.Sample) -> List[Dict[str, Any]]:
        """
        Converts @sample to list of dictionaries. Each dictionary corresponds to one sampled entity,
        with keys equal to attribute names and values corresponding to attribute values.
        """
        result = []
        for entity, values in sample.entities.items():
            for entity_value in values:
                result.append(SampleFormatter.__format_entity(entity, entity_value, sample))
        return result

    @staticmethod
    def __format_entity(entity: Entity, value: EntityValue, sample: REDAG.Sample) -> Dict[str, Any]:
        return {**SampleFormatter.__format_entity_non_reference_attrs(entity, value),
                **SampleFormatter.__format_referenced_entities_ids(entity, value, sample)}

    @staticmethod
    def __format_entity_non_reference_attrs(entity: Entity, value: EntityValue) -> Dict[str, Any]:
        entity_dict = {"entity": entity.__name__}
        for attr, attr_type in RedagAnnotationsProcessor.get_entity_attributes(entity).items():
            if attr_type == ObjectID:
                entity_dict["REDAG_id"] = value.__getattribute__(attr).id
            elif type(attr_type) == ReferenceMetaClass:
                # References are handled separately
                continue
            else:
                entity_dict[attr] = str(value.__getattribute__(attr))
        return entity_dict

    @staticmethod
    def __format_referenced_entities_ids(entity: Entity, entity_value: Any, sample: REDAG.Sample) -> Dict[str, Any]:
        """
            Gathers any reference attributes @entity or its ancestors (i.e. entities referenced by it or
            entities referenced by entities referenced by it etc.) have and stores their values in dictionary.
        """
        result = {}
        for reference, ref_type in get_entity_references(entity).items():
            ref_val = entity_value.__getattribute__(reference)
            parent_entity = [x for x in sample.entities[ref_val.referenced_type] if ref_val.referenced_id == get_object_id(x)][0]
            result = {**result,
                      **SampleFormatter.__format_referenced_entities_ids(ref_val.referenced_type, parent_entity, sample),
                      reference: str(get_object_id(parent_entity))}
        return result
