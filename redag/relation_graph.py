from typing import Generator
import networkx

from redag.entity.entity import get_entity_references, Entity


class RelationGraph(networkx.DiGraph):
    """
    Stores DAG of relations among REDAG entities.
    Process of adding nodes and linking them is separated.
    First all nodes should be added as detached nodes through @add_node method.
    Then, @link_nodes should be called to build the graph.
    """
    def __init__(self, **attr):
        super().__init__(**attr)
        self.linked = False
        self.entity_to_node = {}

    def add_node(self, cls: Entity, **attr):
        """
        Adds @cls as a detached node in the graph.
        """
        super().add_node(cls)

    def link_nodes(self):
        """
        Creates edges between nodes which reference each other.
        """
        if not self.linked:
            self.linked = True
            for node in self.nodes:
                self.__link(node)

    def topological_sort(self) -> Generator[Entity, Entity, None]:
        return networkx.topological_sort(self)

    def __link(self, cls: Entity):
        for value in get_entity_references(cls).values():
            self.add_edge(value.referenced_type, cls)
