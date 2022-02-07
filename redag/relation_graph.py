from typing import Any

from networkx import DiGraph

from redag.links import Reference


def _is_linkable_type(attribute: Any) -> bool:
    return isinstance(attribute, Reference)


class RelationGraph(DiGraph):
    def __init__(self):
        super().__init__()
        self.__dimensions = []
        self.__facts = []

    def add_node(self, cls, **attr):
        self.add_node(cls)
        self.__link(cls)

    def __link(self, cls):
        # TODO do somethign about the string key
        for attr, value in cls.__dict__["__entity_attributes__"]:
            if _is_linkable_type(value):
                self.add_edge(value.entity, cls)
