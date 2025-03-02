Label
=====

.. jinjax:component:: Label(for_: str | None = None, id: str | None = None, class_: str | None = None, content: Any)

    Produce ``<label>`` node.

    :param for: unique identifier of the target element.
    :param id: unique identifier of the element.
    :param class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.LABEL_CLASS`.
    :param content: child node.
