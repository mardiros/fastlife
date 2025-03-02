Password
========

.. jinjax:component:: Password(name: str, id: str | None = None, class_: str | None = None, aria_label: str | None = None, placeholder: str | None = None, autocomplete: Literal['on', 'off', 'current-password', 'new-password'] | None = None, inputmode: Literal['none', 'text', 'numeric'] | None = None, minlength: int | None = None, maxlength: int | None = None, pattern: str | None = None, autofocus: bool = False, required: bool = False, readonly: bool = False)

    Produce ``<input type="password">`` node.

    :param name: submitted name in the form
    :param id: unique identifier of the element.
    :param class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.INPUT_CLASS`.
    :param aria_label: aria-label
    :param placeholder: brief hint to the user as to what kind of information is expected in the field.
    :param autocomplete: Define autocomplete mode
    :param inputmode: Define a virtual keyboard layout
    :param minlength: Minimum length
    :param maxlength: Maximum length
    :param pattern: Must match a pattern
    :param autofocus: Five the focus
    :param required: Mark as required field
    :param readonly: Mark as readonly field
