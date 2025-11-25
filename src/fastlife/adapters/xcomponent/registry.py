from collections.abc import Callable

import venusian
from xcomponent import Catalog
from xcomponent.service.catalog import Component, Function

VENUSIAN_CATEGORY = "fastlife"  # copy/pasta from configurator


class XComponentRegistry:
    """
    Build the XComponent catalog using venusian.

    To avoid a global catalog, we generate the catalog by scanning using
    venusian.
    """

    components: dict[str, Component]

    functions: dict[str, Function]

    def __init__(self) -> None:
        self.components = {}
        self.functions = {}

    def register_xcomponent(self, name: str, component: Component) -> None:
        """Register a xcomponent component to the application template engine."""
        self.components[name] = component

    def register_xfunction(self, name: str, func: Function) -> None:
        """Register a xcomponent function to the application template engine."""
        self.functions[name] = func

    def build_catalog(self) -> Catalog:
        catalog = Catalog()
        for name, component in self.components.items():
            catalog.component(name)(component)

        for name, function in self.functions.items():
            catalog.function(name)(function)
        return catalog


def x_component(name: str | None = None) -> Callable[[Component], Component]:
    """
    Register a component to the XComponent catalog for the application.

    It differ from from @catalog.component decorator of the xcomponent library,
    in the way the catalog is created.
    The fastlife configurator will register the component to a catalog during
    the configuration.

    :param name: override the name of the component, default is the python function
        name.
    """
    component_name = name

    def decorator(wrapped: Component) -> Component:
        def callback(
            scanner: venusian.Scanner,
            name: str,
            ob: Component,
        ) -> None:
            if not hasattr(scanner, VENUSIAN_CATEGORY):
                return  # coverage: ignore
            scanner.fastlife.register_xcomponent(component_name or name, ob)  # type: ignore

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
        return wrapped

    return decorator


def x_function(name: str | None = None) -> Callable[[Function], Function]:
    """
    Register a component to the XComponent function for the application.

    It differ from from @catalog.function decorator of the xcomponent library,
    in the way the catalog is created.
    The fastlife configurator will register the function to a catalog during
    the configuration.

    :param name: override the name of the function, default is the python function name.
    """
    function_name = name

    def decorator(wrapped: Function) -> Function:
        def callback(
            scanner: venusian.Scanner,
            name: str,
            ob: Component,
        ) -> None:
            if not hasattr(scanner, VENUSIAN_CATEGORY):
                return  # coverage: ignore
            scanner.fastlife.register_xfunction(function_name or name, ob)  # type: ignore

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
        return wrapped

    return decorator
