Input
=====

.. jinjax:component:: Input(name: str, value: str = '', type: str = 'text', id: str | None = None, class_: str | None = None, aria_label: str | None = None, placeholder: str | None = None)

    :param name: submitted name in the form
    :param value: submitted value in the form
    :param type: type of the control
    :param id: id
    :param class: css class for the node, defaults to :attr:`fastlife.templating.renderer.constants.Constants.INPUT_CLASS`
    :param aria_label: aria-label
    :param placeholder: brief hint to the user as to what kind of information is expected in the field
