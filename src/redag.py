from dataclasses import dataclass
from typing import Any, Dict, List, Iterator

import networkx

from src.entity.entity import Entity
from src.entity.redag_annotations_processor import RedagAnnotationsProcessor as RAP
from src.relation_graph import RelationGraph
from src.utils import Singleton


class Redag(metaclass=Singleton):
    @dataclass
    class Sample:
        entities: Dict[Entity, List[Any]]

        def merge(self, s: 'Redag.Sample') -> 'Redag.Sample':
            for t, l in s.entities.items():
                self.entities.setdefault(t, []).extend(l)
            return self

    def __init__(self):
        self.__entities = []
        self.__relation_graph = RelationGraph()

    def register_entity(self, cls: Entity) -> None:
        self.__entities.append(cls)
        self.__relation_graph.add_node(cls)

    def generate(self):
        self.__relation_graph.link_nodes()
        while True:
            yield self.__sample(self.__relation_graph.topological_sort(), {})

    def __validate_relation_graph(self) -> None:
        if not networkx.is_directed_acyclic_graph(self.__relation_graph):
            raise ValueError("Relation graph contains cycles!")

    def __sample(self, nodes_to_generate: Iterator[Entity], parents: Dict[Entity, Any]) -> Sample:
        result = Redag.Sample(entities={})

        try:
            node = next(nodes_to_generate)
        except StopIteration:
            return result
        print(node)
        multiplicity = RAP.get_entity_multiplicity_generator(node).__get__(None, node)(parents=parents)
        print(node)
        sampling_state = {"multiplicity": multiplicity}
        for i in range(0, multiplicity):
            value = RAP.get_entity_generator(node).__get__(None, node)(parents=parents, state=sampling_state)
            parents[node] = value
            result.merge(self.__sample(nodes_to_generate, parents)).merge(Redag.Sample(entities={node: [value]}))

        return result
