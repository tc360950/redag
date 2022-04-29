import datetime
import random
from typing import Dict

from redag import REDAG, SampleFormatter, multiplicity_generator_decorator, generator_decorator, Reference, fact, \
    dimension, Dimension


@dimension(max_quantity=10)  # REDAG will generate at most 10 items
class Item(Dimension):
    name: str


@fact()
class SalesOrder:
    quantity: int
    unit_price: float
    order_date: datetime.date
    item_id: Reference[Item]  # SalesOrders have ManyToOne relationship with Items


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
    def sample_invoices_per_sales_order(cls, parents: Dict, **kwargs) -> int:
        """
        Methods decorated with 'multiplicity_generator_decorator'
        are used to define functions which define how many entities of this type should be generated in one sample
        (based on the values of parent entities which are passed in @parents).
        In this case we say that to one sales_order there should correspond between 0 and 4 invoices.
        And the exact number is random.
        """
        return random.randint(0, 4)

    @generator_decorator()
    def sample_invoice(cls, parents: Dict, state: Dict) -> Dict:
        """
        Methods decorated with 'generator_decorator' are responsible for generation of entity
        attributes during sampling.
        @parents is a dict of values of generated parent entities. In this case we can expect that
        parents[SalesOrder] contains instance of SalesOrder class for which we generate invoices.

        @state is a dictionary with one key - multiplicity. It tells us how many invoices should we generate
        (in this case multiplicity will be equal to result of call to @sample_invoices_per_sales_order because
        it's marked as multiplicity_generator_decorator).

        If multiplicity is greater than one, @state will be passed between subsequent calls to sample_invoice.
        In this way we can pass some state between generation of different invoice corresponding to the same sales order.
        """
        total_order_amount = parents[SalesOrder].quantity * parents[SalesOrder].unit_price
        amount_left = state.setdefault("amount_left", total_order_amount)
        invoice_number = state.setdefault("invoice_number", 0) + 1

        if invoice_number == state["multiplicity"]:
            invoice_amount = amount_left
        else:
            invoice_amount = random.random() * amount_left

        # Invoices' amounts must some to amount on the sales order
        # That's why we use state to pass amount which is left for next invoices
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
    # SampleFormatter is a utility class which converts samples to human-readable JSON format
    print(SampleFormatter.format(sample))

    # The result should resemble the following
    """
    [
        {
            "entity": "Invoice",
            "total_amount": "0.26976371928387805",
            "invoice_date": "2022-06-24 11:35:49",
            "invoice_due_date": "2022-06-28 11:35:49",
            "REDAG_id": "425bb4ca-aefe-4022-97b0-326aa65df671",
            "item_id": "23e24330-ca6e-4f33-9067-a9b81c65af11",
            "sales_order_id": "14e241ef-4225-4006-9879-5a59645ed145"
        },
        {
            "entity": "Invoice",
            "total_amount": "0.4425365734990167",
            "invoice_date": "2022-06-24 11:35:49",
            "invoice_due_date": "2022-06-29 11:35:49",
            "REDAG_id": "e1d5a321-f2d1-42aa-b906-a2b58e5cf3f4",
            "item_id": "23e24330-ca6e-4f33-9067-a9b81c65af11",
            "sales_order_id": "14e241ef-4225-4006-9879-5a59645ed145"
        },
        {
            "entity": "WarehouseOrder",
            "quantity": "9",
            "order_date": "2022-06-02 11:35:49",
            "REDAG_id": "0e35ef49-ee88-4bf7-a5d7-11f0a1d22208",
            "item_id": "23e24330-ca6e-4f33-9067-a9b81c65af11",
            "sales_order_id": "14e241ef-4225-4006-9879-5a59645ed145"
        },
        {
            "entity": "SalesOrder",
            "quantity": "3",
            "unit_price": "0.23743343092763158",
            "order_date": "2022-06-24 11:35:49",
            "REDAG_id": "14e241ef-4225-4006-9879-5a59645ed145",
            "item_id": "23e24330-ca6e-4f33-9067-a9b81c65af11"
        },
        {
            "entity": "Item",
            "name": "PMJKUSYTIS",
            "REDAG_id": "23e24330-ca6e-4f33-9067-a9b81c65af11"
        }
    ]
    """
