"""Text components."""

from collections.abc import Mapping

from xcomponent import XNode

from fastlife.adapters.xcomponent.catalog import catalog


@catalog.component
def P(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    <p> html tag rendering

    :param children: child node.
    :param globals: injected root component globals variables.
    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.P_CLASS`.
    """
    return """
    <p id={id} class={class_ or globals.P_CLASS}>
      {children}
    </p>
    """
