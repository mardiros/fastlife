A
=

.. jinjax:component:: A(href: str, id: str | None = None, class_: str | None = None, hx_target: str = '#maincontent', hx_select: str | None = None, hx_swap: str = 'innerHTML show:body:top', hx_push_url: bool = True, disable_htmx: bool = False, content: Any)

    Create html ``<a>`` node with htmx support by default.
    The `hx-get` parameter is set with the href directly unless the
    `disabled-htmx` attribute has been set.

    :param href: target link.
    :param id: unique identifier of the element.
    :param class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.A_CLASS`.
    :param hx_target: target the element for swapping than the one issuing the AJAX request.
    :param hx_select: select the content swapped from response of the AJAX request.
    :param hx_swap: specify how the response will be swapped in relative to the target of an AJAX request.
    :param hx_push_url: replace the browser url with the link.
    :param disable_htmx: do not add any `hx-*` attibute to the link.
    :param content: child node.
