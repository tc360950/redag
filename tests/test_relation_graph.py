from redag.entity.dimension import dimension, Dimension
from redag.entity.fact import fact
from redag.entity.redag_types import Reference
from redag.relation_graph import RelationGraph


@dimension()
class Item1(Dimension):
    pass


@dimension()
class Item2(Dimension):
    pass


@dimension()
class Item3(Dimension):
    pass


@fact()
class Fact1:
    item1: Reference[Item1]
    item2: Reference[Item1]
    item3: Reference[Item1]


@fact()
class Fact2:
    fact_ref: Reference[Fact1]


@fact()
class Fact3:
    fact_ref: Reference[Fact2]


@fact()
class Fact4:
    fact_ref: Reference[Fact1]


def test_relation_graph():
    graph = RelationGraph()
    entities = [Item1, Item2, Item3, Fact1, Fact2, Fact3, Fact4]
    for e in entities:
        graph.add_node(e)

    graph.link_nodes()
    sorted = list(graph.topological_sort())
    assert len(sorted) == 7

    assert all([e in sorted for e in entities])

    entity_to_idx = {}
    for e in entities:
        entity_to_idx[e] = sorted.index(e)

    assert entity_to_idx[Item1] < entity_to_idx[Fact1]
    assert entity_to_idx[Item1] < entity_to_idx[Fact2]
    assert entity_to_idx[Item1] < entity_to_idx[Fact3]
    assert entity_to_idx[Item1] < entity_to_idx[Fact4]

    assert entity_to_idx[Fact1] < entity_to_idx[Fact4]
    assert entity_to_idx[Fact1] < entity_to_idx[Fact2]
    assert entity_to_idx[Fact2] < entity_to_idx[Fact3]