Summary
=======

.. jinjax:component:: Summary(id: str | None = None, class_: str | None = None, open: bool = True, content: Any)

    Create html ``<summary>`` node for the :jinjax:component:`Details` component.

    :param id: unique identifier of the element.
    :param class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.SUMMARY_CLASS`.
    :param open: Open or collapse the content of the details.
    :param content: child node.
