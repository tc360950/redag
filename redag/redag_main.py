from dataclasses import dataclass

from redag.relation_graph import RelationGraph

#  is_directed_acyclic_graph

# topological_sort for gen

@dataclass
class Redag:
    relation_graph: RelationGraph
    __dimensions = []
    __facts = []

    def register_dimension(self, cls):
        self.__dimensions.append(cls)
        self.relation_graph.add_node(cls)

    def register_fact(self, cls):
        self.__facts.append(cls)
        self.relation_graph.add_node(cls)