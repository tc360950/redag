from typing import Any, Generator
import networkx

from src.entity.entity import get_entity_references


class RelationGraph(networkx.DiGraph):
    def __init__(self, **attr):
        super().__init__(**attr)
        self.linked = False
        self.entity_to_node = {}

    def add_node(self, cls, **attr):
        super().add_node(cls)

    def link_nodes(self):
        if not self.linked:
            self.linked = True
            for node in self.nodes:
                self.__link(node)

    def topological_sort(self) -> Generator[Any, Any, None]:
        return networkx.topological_sort(self)

    def __link(self, cls):
        for value in get_entity_references(cls).values():
            self.add_edge(value.referenced_type, cls)
