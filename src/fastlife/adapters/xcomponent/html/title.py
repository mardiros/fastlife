"""Titles"""

from collections.abc import Mapping

from xcomponent import XNode

from fastlife.adapters.xcomponent.catalog import catalog


@catalog.component
def H1(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    <h1> html tag rendering

    :param children: child node.
    :param globals: injected root component globals variables.
    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.H1_CLASS`.
    """
    return """
        <h1 id={id} class={class_ or globals.H1_CLASS}>
            {children}
        </h1>
    """


@catalog.component
def H2(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    <h2> html tag rendering

    :param children: child node.
    :param globals: injected root component globals variables.
    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.H2_CLASS`.
    """
    return """
        <h2 id={id} class={class_ or globals.H2_CLASS}>
            {children}
        </h2>
    """


@catalog.component
def H3(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    <h3> html tag rendering

    :param children: child node.
    :param globals: injected root component globals variables.
    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.H3_CLASS`.
    """
    return """
        <h3 id={id} class={class_ or globals.H3_CLASS}>
            {children}
        </h3>
    """


@catalog.component
def H4(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    <h4> html tag rendering

    :param children: child node.
    :param globals: injected root component globals variables.
    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.H4_CLASS`.
    """
    return """
        <h4 id={id} class={class_ or globals.H4_CLASS}>
            {children}
        </h4>
    """


@catalog.component
def H5(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    <h5> html tag rendering

    :param children: child node.
    :param globals: injected root component globals variables.
    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.H5_CLASS`.
    """
    return """
        <h5 id={id} class={class_ or globals.H5_CLASS}>
            {children}
        </h5>
    """


@catalog.component
def H6(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
) -> str:
    """
    <h6> html tag rendering

    :param children: child node.
    :param globals: injected root component globals variables.
    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.H6_CLASS`.
    """
    return """
        <h6 id={id} class={class_ or globals.H6_CLASS}>
            {children}
        </h6>
    """
