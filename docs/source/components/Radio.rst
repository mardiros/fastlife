Radio
=====

.. jinjax:component:: Radio(label: str, name: str, value: str, id: str | None, checked: bool = False, disabled: bool = False, onclick: str | None = None, div_class: str | None = None, class_: str | None = None, label_class: str | None = None)

    Produce a ``<input type="radio">`` with its associated label inside a div.

    :param label: label text associated to the radio
    :param name: name of the submitted
    :param value: value that will be submitted if selected
    :param id: unique identifier of the element.
    :param checked: Tick the radio button
    :param disabled: Mark the radio button as disabled
    :param onclick: execute some javascript while clicking
    :param div_class: css class for the div node, defaults to :attr:`fastlife.templates.constants.Constants.RADIO_DIV_CLASS`
    :param class: css class for the input node, defaults to :attr:`fastlife.templates.constants.Constants.RADIO_INPUT_CLASS`
    :param label_class: css class for the label node, defaults to :attr:`fastlife.templates.constants.Constants.RADIO_LABEL_CLASS`
