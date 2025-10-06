"""Navigation component."""

from collections.abc import Mapping

from xcomponent import XNode

from fastlife.adapters.xcomponent.catalog import catalog


@catalog.component
def A(
    href: str,
    children: XNode,
    globals: Mapping[str, str],
    id: str | None = None,
    class_: str | None = None,
    hx_target: str = "#maincontent",
    hx_select: str | None = None,
    hx_swap: str = "innerHTML show:body:top",
    hx_push_url: bool | str = True,
    hx_get: str | None = None,
    hx_disable: bool | None = None,
    hx_disabled_elt: str | None = None,
) -> str:
    """
    Create html ``<a>`` node with htmx support by default.
    The `hx-get` parameter is set with the href directly unless the
    `disabled-htmx` attribute has been set.

    :param href: Target link.
    :param id: Unique identifier of the element.
    :param class_: CSS class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.A_CLASS`.
    :param hx_target: Target the element for swapping than the one issuing
        the AJAX request.
    :param hx_select: Select the content swapped from the response of the AJAX request.
    :param hx_swap: Specify how the response will be swapped in relative to the target
        of an AJAX request.
    :param hx_push_url: Replace the browser URL with the link.
    :param hx_get: Override the target link only for htmx request for component
        rendering. href will be used if None.
    """

    return """
        <a
            href={href}
            id={id}
            hx-disable={hx_disable}
            hx-disabled-elt={hx_disabled_elt}
            hx-get={hx_get or href}
            hx-target={hx_target}
            hx-swap={hx_swap}
            hx-push-url={
                if isbool(hx_push_url) {
                    if hx_push_url { "true" } else { false }
                }
                else { hx_push_url }
            }
            hx-select={hx_select}
            class={class_ or globals.A_CLASS}
        >
            {children}
        </a>
    """
