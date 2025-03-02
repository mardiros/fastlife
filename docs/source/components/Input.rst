Input
=====

.. jinjax:component:: Input(name: str, value: str = '', type: str = 'text', id: str | None = None, class_: str | None = None, aria_label: str | None = None, placeholder: str | None = None, inputmode: Literal['none', 'text', 'decimal', 'numeric', 'tel', 'search', 'email', 'url'] | None = None, autocomplete: Literal['on', 'off', 'name', 'username', 'current-password', 'new-password', 'one-time-code', 'email', 'tel', 'organization', 'street-address', 'address-line1', 'address-line2', 'address-line3', 'postal-code', 'country', 'country-name', 'cc-name', 'cc-number', 'cc-exp', 'cc-csc', 'tel-country-code', 'tel-national', 'tel-area-code', 'tel-local', 'tel-extension', 'bday', 'bday-day', 'bday-month', 'bday-year', 'transaction-amount', 'transaction-currency'] | None = None, autofocus: bool = False)

    Produce ``<input>`` node.

    :param name: submitted name in the form
    :param value: submitted value in the form
    :param type: type of the control
    :param id: unique identifier of the element.
    :param class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.INPUT_CLASS`.
    :param aria_label: aria-label
    :param placeholder: brief hint to the user as to what kind of information is expected in the field.
    :param inputmode: Define a virtual keyboard layout
    :param autocomplete: Define autocomplete mode
    :param autofocus: Five the focus
