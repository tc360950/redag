from datetime import datetime

from redag.entity import entity_decorator

__dimension_allowed_types__ = [str, int, float, datetime]

from redag.redag_main import Redag


def dimension(redag: Redag, max_quantity: int):
    def f(cls):
        entity_decorator(__dimension_allowed_types__)(cls)
        redag.register_dimension(cls)
        return cls
    return f