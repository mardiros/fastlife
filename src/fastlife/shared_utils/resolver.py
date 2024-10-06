"""Resolution of python objects for dependency injection and more."""

import importlib.util
import inspect
from pathlib import Path
from types import ModuleType, UnionType
from typing import Any, Union


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
    except AttributeError as exc:
        raise ValueError(
            f"Attribute {attr_name} not found in module {module_name}"
        ) from exc

    return attr


def resolve_extended(value: str) -> UnionType:
    """Resolve many types separed by a pipe (``|``), the union separator."""
    values = value.split("|")
    if len(values) == 1:
        return resolve(value)
    types = [resolve(t) for t in values if t != "builtins:NoneType"]
    return Union[tuple(types)]  # type: ignore # noqa: UP007


def resolve_path(value: str) -> str:
    """
    Resole a path on the disk from a python package name.

    This helper is used to find static assets inside a python package.
    """
    package_name, resource_name = value.split(":", 1)
    spec = importlib.util.find_spec(package_name)
    if not spec or not spec.origin:
        raise ValueError(f"{value} not found")
    package_path = spec.origin
    full_path = Path(package_path).parent / resource_name
    return str(full_path)


def resolve_package(mod: ModuleType) -> ModuleType:
    """
    Return the
    [regular package](https://docs.python.org/3/glossary.html#term-regular-package)
    of a module or itself if it is the ini file of a package.

    """

    # Compiled package has no __file__ attribute, ModuleType declare it as NoneType
    if not hasattr(mod, "__file__") or mod.__file__ is None:
        return mod

    module_path = Path(mod.__file__)
    if module_path.name == "__init__.py":
        return mod

    parent_module_name = mod.__name__.rsplit(".", 1)[0]
    parent_module = importlib.import_module(parent_module_name)
    return parent_module


def _strip_left_dots(s: str) -> tuple[str, int]:
    stripped_string = s.lstrip(".")
    num_stripped_dots = len(s) - len(stripped_string)
    return stripped_string, num_stripped_dots - 1


def _get_parent(pkg: str, num_parents: int) -> str:
    if num_parents == 0:
        return pkg
    segments = pkg.split(".")
    return ".".join(segments[:-num_parents])


def resolve_maybe_relative(mod: str, stack_depth: int = 1) -> ModuleType:
    """
    Resolve a module, maybe relative to the stack frame and import it.

    :param mod: the module to import. starts with a dot if it is relative.
    :param stack_depth: relative to which module in the stack.
        used to do an api that call it instead of resolve the module directly.
    :return: the imported module
    """
    if mod.startswith("."):
        caller_module = inspect.getmodule(inspect.stack()[stack_depth][0])
        # we could do an assert here but caller_module could really be none ?
        parent_module = resolve_package(caller_module)  # type: ignore
        package = parent_module.__name__
        mod, count = _strip_left_dots(mod)
        package = _get_parent(package, count)
        mod = f"{package}.{mod}".rstrip(".")

    module = importlib.import_module(mod)
    return module
