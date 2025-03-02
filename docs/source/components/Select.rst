Select
======

.. jinjax:component:: Select(name: str, id: str | None = None, class_: str | None = None, multiple: bool = False, content: Any)

    Create html ``<select>`` node.

    :param name: name of the submitted
    :param id: unique identifier of the element.
    :param class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.SELECT_CLASS`.
    :param multiple: Mark as multiple
    :param content: child node.
