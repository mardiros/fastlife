Checkbox
========

.. jinjax:component:: Checkbox(name: str, id: str | None = None, class_: str | None = None, value: str | None = None, checked: bool = False)

    Create html ``<input type="checkbox" />`` node.

    :param name: Name of the checkbox
    :param id: unique identifier of the element.
    :param class: css class for the node, defaults to :attr:`fastlife.templating.renderer.constants.Constants.CHECKBOX_CLASS`
    :param value: http submitted value if the checkbox is checked
    :param checked: Initialized the checkbox as ticked
