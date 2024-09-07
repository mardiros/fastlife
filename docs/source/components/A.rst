A
=

.. jinjax:component:: A(href: str, hx_target: str = '#maincontent', hx_select: str | None = None, hx_swap: str = 'innerHTML show:body:top', hx_push_url: bool = True, disable_htmx: bool = False, content: Any)

    Create html `<a>` node with htmx support by default.
    The `hx-get` parameter is set with the href directly unless the
    `disabled-htmx` attribute has been set.

    :param href: target link
    :param hx_target:
    :param hx_select:
    :param hx_swap:
    :param hx_push_url:
    :param disable_htmx:
    :param content: child none
