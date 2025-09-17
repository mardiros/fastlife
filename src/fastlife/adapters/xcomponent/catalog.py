from typing import Any

from xcomponent import Catalog

catalog = Catalog()
"""The catalog to register components."""


@catalog.function(name="len")
def length(iterable: Any) -> int:
    return len(iterable)
