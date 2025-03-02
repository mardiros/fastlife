pydantic_form.FatalError
========================

.. jinjax:component:: pydantic_form.FatalError(message: str | None, class_: str | None = None, icon_class: str | None = None, text_class: str | None = None)

    display an error for a field.

    :param message: error message
    :param class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.FATAL_ERROR_CLASS`.
    :param icon_class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.FATAL_ERROR_ICON_CLASS`.
    :param text_class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.FATAL_ERROR_TEXT_CLASS`.
