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
    hx_push_url: bool = True,
    hx_get: str | None = None,
    hx_disable: bool | None = None,
    hx_disabled_elt: str | None = None,
) -> str:
    """
    Create html ``<a>`` node with htmx support by default.
    The `hx-get` parameter is set with the href directly unless the
    `disabled-htmx` attribute has been set.
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
            hx-push-url={hx_push_url}
            hx-select={hx_select}
            class={class_ or globals.A_CLASS}
        >
            {children}
        </a>
    """
