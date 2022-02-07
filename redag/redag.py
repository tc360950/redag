from dataclasses import dataclass

from redag.relation_graph import RelationGraph


@dataclass
class Redag:
    relation_graph: RelationGraph
    __dimensions = []
    __facts = []

    def register_dimension(self, cls):
        self.__dimensions.append(cls)
        pass

    def register_fact(self, cls):
        self.__facts.append(cls)
        pass