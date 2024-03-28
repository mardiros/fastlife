import importlib.util
from pathlib import Path
from typing import Any, Type, Union


def resolve(value: str) -> Any:
    """return the attr from the syntax: package.module:attr."""
    module_name, attr_name = value.split(":", 2)
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        raise ValueError(f"Module {module_name} not found")
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        # I can't figure out when the spec.loader is None,
        # just relying on typing here
        raise ValueError("No loader on spec")  # coverage: ignore
    spec.loader.exec_module(module)

    try:
        attr = getattr(module, attr_name)
    except AttributeError:
        raise ValueError(f"Attribute {attr_name} not found in module {module_name}")

    return attr


def resolve_extended(value: str) -> Type[Any]:
    values = value.split("|")
    if len(values) == 1:
        return resolve(value)
    types = [resolve(t) for t in values if t != "builtins:NoneType"]
    return Union[tuple(types)]  # type: ignore


def resolve_path(value: str) -> str:
    package_name, resource_name = value.split(":", 1)
    spec = importlib.util.find_spec(package_name)
    if not spec or not spec.origin:
        raise ValueError(f"{value} not found")
    package_path = spec.origin
    full_path = Path(package_path).parent / resource_name
    return str(full_path)
