from redag.dimension import dimension
from redag.entity import generator
from redag.fact import fact
from redag.links import EntityReference
from redag.redag_main import Redag
from redag.relation_graph import RelationGraph

redag = Redag(RelationGraph())


@dimension(redag=redag, max_quantity=100)
class Customer:
    cde2: int
    value: int
    abc: int

    @generator(name="value")
    def generate_value(cls, values, **kwargs):
        pass


@fact(redag=redag)
class Invoice:
    item_id: EntityReference(Customer)
    value: int


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(Customer.__dict__)
    x = Customer.__generator_function__()
    print(x.__dict__)
    print(redag.relation_graph.nodes)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
