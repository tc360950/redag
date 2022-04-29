from redag import REDAG, SampleFormatter
from redag.entity.dimension import dimension, Dimension
from redag.entity.fact import fact
from redag.entity.redag_types import Reference


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
    item2: Reference[Item2]
    item3: Reference[Item3]


@fact()
class Fact2:
    fact_ref: Reference[Fact1]


@fact()
class Fact3:
    fact_ref2: Reference[Fact2]


@fact()
class Fact4:
    fact_ref3: Reference[Fact1]



def test_format():
    sample = next(REDAG().generate())
    formatted_sample = SampleFormatter.format(sample)

    assert len(formatted_sample) == 7

    for entity in formatted_sample:
        if "Item" in entity["entity"]:
            assert len(entity) == 2
        elif entity["entity"] == "Fact1":
            assert len(entity) == 2 + 3 # references to three items
            assert all(a in entity for a in ["item1", "item2", "item3"])
            assert len(set(entity[a] for a in ["item1", "item2", "item3"])) == 3
        elif entity["entity"] == "Fact3":
            assert len(entity) == 2 + 3 + 2  # indicrect references to three items and 2 facts