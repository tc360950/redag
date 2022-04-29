import datetime
import random
from typing import Dict

from redag import REDAG, SampleFormatter, multiplicity_generator_decorator, generator_decorator, Reference, fact, dimension, Dimension


@dimension(max_quantity=1)
class Item(Dimension):
    name: str


@fact()
class SalesOrder:
    quantity: int
    unit_price: float
    order_date: datetime.date
    item_id: Reference[Item]


@fact()
class WarehouseOrder:
    quantity: int
    order_date: datetime.date
    sales_order_id: Reference[SalesOrder]


@fact()
class Invoice:
    total_amount: float
    invoice_date: datetime.date
    invoice_due_date: datetime.date
    sales_order_id: Reference[SalesOrder]

    @multiplicity_generator_decorator()
    def sample_invoices_per_sales_order(cls, *args, **kwargs) -> int:
        return random.randint(0, 4)

    @generator_decorator()
    def sample_invoice(cls, parents: Dict, state: Dict) -> Dict:
        total_order_amount = parents[SalesOrder].quantity * parents[SalesOrder].unit_price
        amount_left = state.setdefault("amount_left", total_order_amount)
        invoice_number = state.setdefault("invoice_number", 0) + 1

        if invoice_number == state["multiplicity"]:
            invoice_amount = amount_left
        else:
            invoice_amount = random.random() * amount_left

        state["amount_left"] = state["amount_left"] - invoice_amount
        state["invoice_number"] = invoice_number
        invoice_date = parents[SalesOrder].order_date
        return {
            "total_amount": invoice_amount,
            "invoice_date": invoice_date,
            "invoice_due_date": invoice_date + datetime.timedelta(days=random.randint(1, 10))
        }


if __name__ == "__main__":
    sample = next(REDAG().generate())
    print(SampleFormatter.format(sample))
