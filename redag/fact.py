from datetime import datetime

from redag.entity import entity_decorator
from redag.links import EntityReference, OneToManyReference

__fact_allowed_types__ = [str, int, float, datetime, EntityReference, OneToManyReference]

from redag.redag import Redag


def fact(redag: Redag):
    def f(cls):
        entity_decorator(__fact_allowed_types__)(cls)
        redag.register_fact(cls)
        return cls
    return f