"""Inline templates."""

from typing import ClassVar

from pydantic import BaseModel


class InlineTemplate(BaseModel):
    """
    Inline templates are used to encourage the location of behavior and the view typing.

    Pages produce templates that are not reusable and don't need to be reusable
    in there essence, they don't need to be in a component library.
    They use a component lirary to stay small but contains a view logic
    tighly coupled with the view and its code can stay in the same module of that view.
    """

    template: ClassVar[str]
    """The template string to render."""
