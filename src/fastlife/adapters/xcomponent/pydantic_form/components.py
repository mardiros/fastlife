from xcomponent import XNode

from fastlife.adapters.xcomponent.catalog import catalog


@catalog.component
def ErrorText(
    text: str,
    class_: str,
) -> str:
    """
    display an error for a field.

    :param text: error message
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.ERROR_CLASS`.
    """
    return """
        <span class={class_ or globals.ERROR_CLASS}>{text}</span>
    """


@catalog.component
def OptionalErrorText(
    text: str | None,
    class_: str | None = None,
) -> str:
    """
    display an error for a field.

    :param text: error message
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.ERROR_CLASS`.
    """
    return """
    <>
        {
            if text {
                <ErrorText text={text} class={class_} />
            }
        }
    </>
    """


@catalog.component
def FatalError(
    message: str | None,
    class_: str | None = None,
    icon_class: str | None = None,
    text_class: str | None = None,
) -> str:
    """
    display an error for a field.

    :param message: error message
    :param class_: css class for the node, defaults to
        :attr:`fastlife.template_globals.Globals.FATAL_ERROR_CLASS`.
    :param icon_class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.FATAL_ERROR_ICON_CLASS`.
    :param text_class: css class for the node, defaults to :attr:`fastlife.template_globals.Globals.FATAL_ERROR_TEXT_CLASS`.
    """
    return """
    <>
    {
      if message {
        <div class={class_ or globals.FATAL_ERROR_CLASS} role="alert">
          <Icon name="fire" class={icon_class or globals.FATAL_ERROR_ICON_CLASS} />
          <span class={text_class or globals.FATAL_ERROR_TEXT_CLASS}>{message}</span>
        </div>
      }
    }
    </>
    """


@catalog.component
def Hint(text: str | None) -> str:
    """
    Display a hint message for a field.

    :param text: hint text.
    """
    return """
    <>
    {
        if text {
            <span class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
                {text}
            </span>
        }
    }
    </>
    """


@catalog.component
def Widget(
    widget_id: str,
    removable: bool,
    children: XNode,
) -> str:
    """
    Base component for widget.

    :param widget_id: widget to display.
    :param removable: Set to true to add a remove button
    """
    return """
    <div id={widget_id + "-container"}>
      {children}
      {
        if removable {
          <Button type="button"
            onclick={"document.getElementById('" + widget_id + "-container').remove()"}
            >
            Remove
         </Button>
        }
      }
    </div>
    """
