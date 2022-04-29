import pytest

from typing import Dict

from redag import REDAG
from redag.entity.dimension import dimension, Dimension
from redag.entity.entity import multiplicity_generator_decorator, get_object_id, generator_decorator
from redag.entity.fact import fact
from redag.entity.redag_types import Reference


@dimension(max_quantity=10)  # REDAG will generate at most 10 items
class Item(Dimension):
    name: str


@fact()
class SalesOrder:
    item_id: Reference[Item]  # SalesOrders have ManyToOne relationship with Items


@fact()
class Invoice:
    sales_order_id: Reference[SalesOrder]
    num: int

    @multiplicity_generator_decorator()
    def sample_invoices_per_sales_order(cls, parents: Dict, **kwargs) -> int:
        return 4

    @generator_decorator()
    def generator(cls, parents: Dict, state: Dict, **kwargs):
        num = state.setdefault("num", 0)
        state["num"] += 1
        return {
            "num": num
        }


def test_sampling():
    sample = next(REDAG().generate())
    assert len(sample.entities) == 1 + 1 + 1  # three types of entities should be generated
    assert len(sample.entities[Invoice]) == 4
    # Invoices should reference the sames sales order
    assert all([i.sales_order_id.referenced_id.id == get_object_id(sample.entities[SalesOrder][0]).id for i in
                sample.entities[Invoice]])

    assert [i.num for i in sample.entities[Invoice]] == [0, 1, 2, 3]
