"""
Widget for field of type bool.
"""

from .base import Widget


class BooleanWidget(Widget[bool]):
    """
    Widget for field of type bool.
    """

    template = """
    <Widget widget_id={id} removable={removable}>
      <div class="pt-4">
        <div class="flex items-center">
         <Checkbox name={name} id={id} checked={value} value="1" />
         <Label for={id} class="ms-2 text-base text-neutral-900 dark:text-white">
            {globals.gettext(title)}
          </Label>
        </div>
       <OptionalErrorText text={error} />
      </div>
    </Widget>
    """
