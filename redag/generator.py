from collections import Callable
from dataclasses import dataclass
from typing import Union


@dataclass
class Generator:
    attr_name: Union[str, None]
    func: Callable
