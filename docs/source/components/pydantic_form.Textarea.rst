pydantic_form.Textarea
======================

.. jinjax:component:: pydantic_form.Textarea(widget: fastlife.templating.renderer.widgets.text.TextareaWidget)

    Render textarea widget for field of type text of event sequence.

    ::

    from fastlife.templating.renderer.widgets.text import TextareaWidget
    from pydantic import BaseModel, Field, field_validator

    class TagsForm(BaseModel):

    tags: Annotated[Sequence[str], TextareaWidget] = Field(
    default_factory=list,
    title="Tags",
    description="One tag per line",
    )

    @field_validator("tags", mode="before")
    def split(cls, s: Any) -> Sequence[str]:
    return s.split() if s else []

    :param widget: widget to display.
