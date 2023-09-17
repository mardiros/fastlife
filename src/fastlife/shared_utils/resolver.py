import importlib.util
from typing import Any


def resolve(value: str) -> Any:
    """return the attr from the syntax: package.module:attr."""
    module_name, attr_name = value.split(":", 2)
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        raise ValueError(f"Module {module_name} not found.")
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ValueError("No loader on spec")
    spec.loader.exec_module(module)

    try:
        attr = getattr(module, attr_name)
    except AttributeError:
        raise ValueError(f"Attribute {attr_name} not found in module {module_name}.")

    return attr
