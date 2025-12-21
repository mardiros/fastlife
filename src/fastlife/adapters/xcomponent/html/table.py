"""Table components."""

from collections.abc import Mapping

from xcomponent import XNode

from fastlife.adapters.xcomponent.registry import BUILTINS_CATALOG_NS, x_component


@x_component(namespace=BUILTINS_CATALOG_NS)
def Table(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    html ``<table>`` node.

    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.TABLE_CLASS`.
    """
    return """
    <table id={id} class={class_ or globals.TABLE_CLASS}>
        {children}
    </table>
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Thead(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    html ``<thead>`` node.

    :param id: unique identifier of the element.
    :param class_: css class for the node
    """
    return """
    <thead id={id} class={class_}>
        {children}
    </thead>
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Tbody(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    html ``<tbody>`` node.

    :param id: unique identifier of the element.
    :param class_: css class for the node
    """
    return """
    <tbody id={id} class={class_}>
        {children}
    </tbody>
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Tfoot(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    html ``<tfoot>`` node.

    :param id: unique identifier of the element.
    :param class_: css class for the node
    """
    return """
    <tfoot id={id} class={class_}>
        {children}
    </tfoot>
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Th(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    html ``<th>`` node.

    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.TH_CLASS`.
    """
    return """
    <th id={id} class={class_ or globals.TH_CLASS}>
        {children}
    </th>
    """


@x_component(namespace=BUILTINS_CATALOG_NS)
def Td(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    html ``<td>`` node.

    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.TD_CLASS`.
    """
    return """
    <td id={id} class={class_ or globals.TD_CLASS}>
        {children}
    </td>
    """
