Details
=======

.. jinjax:component:: Details(id: str | None = None, open: bool = True, content: Any)

    Produce a ``<details>`` html node in order to create a collapsible box.

    .. code-block:: html

      <Details>
        <Summary :id="my-summary">
          <H3 :class="H3_SUMMARY_CLASS">A title</H3>
        </Summary>
        <div>
          Some content
        </div>
      </Details>

    :param id: unique identifier of the element.
    :param open: open/close state.
    :param content: child node.
