"""Collapsible components, using details/summary."""

from collections.abc import Mapping

from xcomponent import XNode

from fastlife.adapters.xcomponent.catalog import catalog


@catalog.component
def Details(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
    open: bool = True,
) -> str:
    """
    Produce a ``<details>`` html node in order to create a collapsible box.

    .. code-block:: html

      <Details>
        <Summary id="my-summary">
          <H3 class={globals.H3_SUMMARY_CLASS}>A title</H3>
        </Summary>
        <div>
          Some content
        </div>
      </Details>

    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.DETAILS_CLASS`.
    :param open: open/close state.
    """
    return """
    <details id={id} class={class_ or globals.DETAILS_CLASS} open={open}>
        {children}
    </details>
    """


@catalog.component
def Summary(
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
    open: bool = True,
) -> str:
    """
    Create html ``<summary>`` node for the
    :func:`fastlife.adapters.xcomponent.html.collapsible.Details` component.

    :param id: unique identifier of the element.
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.SUMMARY_CLASS`.
    :param open: Open or collapse the content of the details.
    """
    return """
    <summary id={id} class={class_ or globals.SUMMARY_CLASS}
      style="list-style: none; -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none;"
      onclick={"document.getElementById('" + id + "-icon').classList.toggle('rotate-90')"}>
      <Icon name="chevron-right" id={id + '-icon'}
        class={
            if open {
                "w-8 h-8 transform transition-transform duration-300 rotate-90"
            }
            else {
                "w-8 h-8 transform transition-transform duration-300"
            }
        } />
        { children }
    </summary>
    """
