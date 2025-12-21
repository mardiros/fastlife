from collections import defaultdict
from collections.abc import Callable

import venusian
from xcomponent import Catalog
from xcomponent.service.catalog import Component, Function

VENUSIAN_CATEGORY = "fastlife"  # copy/pasta from configurator
DEFAULT_CATALOG_NS = "app"
BUILTINS_CATALOG_NS = "builtins"
PYDANTICFORM_CATALOG_NS = "pydantic_form"

NSCatalog = dict[str, Catalog]

CatalogDict = dict[str, Component]
NSCatalogDict = dict[str, CatalogDict]


class XComponentRegistry:
    """
    Build the XComponent catalog using venusian.

    To avoid a global catalog, we generate the catalog by scanning using
    venusian.
    """

    components: NSCatalogDict

    functions: dict[str, Function]

    def __init__(self) -> None:
        self.components = defaultdict(dict)
        self.components[DEFAULT_CATALOG_NS] = {}  # ensure the app namespace exists
        self.functions = {}

    def register_xcomponent(
        self,
        name: str,
        component: Component,
        *,
        namespace: str,
    ) -> None:
        """Register a xcomponent component to the application template engine."""
        self.components[namespace][name] = component

    def register_xfunction(self, name: str, func: Function) -> None:
        """Register a xcomponent function to the application template engine."""
        self.functions[name] = func

    def build_catalogs(self) -> NSCatalog:
        catalogs: NSCatalog = {ns: Catalog() for ns in self.components.keys()}

        # we ensure we have a builtin catalog
        builtin_catalog: Catalog = catalogs.get(BUILTINS_CATALOG_NS) or Catalog()
        for name, component in self.components.get(BUILTINS_CATALOG_NS, {}).items():
            # we don't backref the builtins components to other namespace
            builtin_catalog.component(name, use=catalogs)(component)
        catalogs[BUILTINS_CATALOG_NS] = builtin_catalog

        for name, function in self.functions.items():
            builtin_catalog.function(name)(function)

        for ns, components in self.components.items():
            if ns == BUILTINS_CATALOG_NS:  # the default ns is process first and appart.
                continue

            ctlg = catalogs[ns]

            # we copy all the builtins components to all namespaces
            for name, component in self.components.get(BUILTINS_CATALOG_NS, {}).items():
                ctlg.component(name, use={})(component)

            for name, component in components.items():
                ctlg.component(name, use=catalogs)(component)

            for name, function in self.functions.items():
                ctlg.function(name)(function)

            catalogs[ns] = ctlg

        return catalogs


def x_component(
    namespace: str = DEFAULT_CATALOG_NS,
    name: str | None = None,
) -> Callable[[Component], Component]:
    """
    Register a component to the XComponent catalog for the application.

    It differ from from @catalog.component decorator of the xcomponent library,
    in the way the catalog is created.
    The fastlife configurator will register the component to a catalog during
    the configuration.

    :param name: override the name of the component, default is the python function
        name.
    :param use: import a catalog as a namespace components.
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
            scanner.fastlife.register_xcomponent(  # type: ignore
                component_name or name,
                ob,
                namespace=namespace,
            )

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
