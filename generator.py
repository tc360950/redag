from collections import Callable
from dataclasses import dataclass
from typing import Union

__GENERATOR_CONFIG_KEY__ = "__generator_config__"


@dataclass
class Generator:
    attr_name: Union[str, None]
    func: Callable


def generator(**kwargs):
    # If the name is not provided we treat it as all attributes generator
    name = kwargs.get("name", None)

    def dec(f: Callable) -> classmethod:
        f_cls = f if isinstance(f, classmethod) else classmethod(f)
        setattr(
            f_cls,
            __GENERATOR_CONFIG_KEY__,
            Generator(attr_name=name, func=f_cls.__func__)
        )
        return f_cls

    return dec
