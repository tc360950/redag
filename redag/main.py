

from entity import entity, generator


@entity(items=2000)
class Customer:
    cde2: int
    value: int
    abc: int

    @generator(name="value")
    def generate_value(cls, values):
        pass

#@fact
#class Invoice:
 #   item_id: EntityRef(Item)
  #  value: int
   # sales_order: OneToMany(SalesOrder)
   # customer_id: EntityRef(Customer)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(Customer.__dict__)
    x = Customer.__generator_function__()
    print(x.__dict__)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
