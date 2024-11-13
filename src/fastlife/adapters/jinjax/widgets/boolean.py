"""
Widget for field of type bool.
"""

from .base import Widget


class BooleanWidget(Widget[bool]):
    """
    Widget for field of type bool.
    """

    template = """
    <pydantic_form.Widget :widget_id="id" :removable="removable">
      <div class="pt-4">
        <div class="flex items-center">
         <Checkbox :name="name" :id="id" :checked="value" value="1" />
         <Label :for="id" class="ms-2 text-base text-neutral-900 dark:text-white">
            {{title|safe}}
          </Label>
        </div>
       <pydantic_form.Error :text="error" />
      </div>
    </pydantic_form.Widget>
    """
