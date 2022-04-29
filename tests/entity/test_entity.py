from redag.entity.dimension import dimension, Dimension
from redag.entity.entity import generator_decorator, multiplicity_generator_decorator
from redag.entity.redag_annotations_processor import RedagAnnotationsProcessor
from redag.entity.redag_types import Reference
from redag.entity.fact import fact
from redag.redag import REDAG


def test_simple_entity_creation():
    @dimension()
    class SimpleEntity(Dimension):
        amount: float
        quantity: int

        @generator_decorator()
        def generate(cls, **kwargs):
            return {
                "amount": 10.0,
                "quantity": 1
            }

    @fact()
    class SimpleFact:
        amount: float
        simple_entity_id: Reference[SimpleEntity]

        # @generator_decorator()
        # def generate(cls, **kwargs):
        #    return {
        #        "amount": kwargs['parents'][SimpleEntity].amount,
        #    }

    @fact()
    class SimpleFact2:
        amount: float
        simple_fact_id: Reference[SimpleFact]

        @multiplicity_generator_decorator()
        def generate(self, parents, state) -> int:
            return 3

        # @generator_decorator()
        # def generate(cls, **kwargs):
        #    return {
        #        "amount": kwargs['parents'][SimpleEntity].amount,
        #    }
    se = SimpleEntity(amount=11.0, quantity=2)
    se2 = SimpleFact.__dict__['__REDAG_KEY__']['__generator_function__'].__func__(SimpleFact,
                                                                                  parents={SimpleEntity: se})
    i = 0

    dupy = [RedagAnnotationsProcessor.get_entity_generator(SimpleEntity).__get__(None, SimpleEntity)(parents={})for i in range(0, 20)]
    print(dupy)
    #x =  Redag().generate()
    import networkx as nx
    G = nx.DiGraph([(1, 2), (2, 3), (2, 4), (4, 5), (3, 5)])
    print(nx.is_directed_acyclic_graph(G))
    next(REDAG().generate())
    #for en in Redag().generate():
     #   print(en)