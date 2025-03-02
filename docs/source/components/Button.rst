Button
======

.. jinjax:component:: Button(type: Literal['submit', 'button', 'reset'] = 'submit', id: str | None = None, class_: str | None = None, name: str = 'action', value: str = 'submit', hidden: bool = False, aria_label: str | None = None, onclick: str | None = None, hx_target: str | None = None, hx_swap: str | None = None, hx_select: str | None = None, hx_after_request: str = '', hx_vals: str | None = None, hx_confirm: str | None = None, hx_get: str | None = None, hx_post: str | None = None, hx_put: str | None = None, hx_patch: str | None = None, hx_delete: str | None = None, hx_params: str | None = None, hx_push_url: bool = false, full_width: str = false, content: Any)

    Create html ``<button>`` node.

    :param type: Define button behavior.
    :param id: unique identifier of the element.
    :param class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.BUTTON_CLASS`.
    :param name:
    :param value:
    :param hidden:
    :param aria_label:
    :param onclick:
    :param hx_target:
    :param hx_swap:
    :param hx_select:
    :param hx_after_request: Produce the hx-on::after-request
    :param hx_vals:
    :param hx_confirm:
    :param hx_get:
    :param hx_post:
    :param hx_put:
    :param hx_patch:
    :param hx_delete:
    :param hx_params:
    :param hx_push_url: Replace the browser url by the ajax request
    :param full_width: Append tailwind class w-full to get full width
    :param content: child node.
