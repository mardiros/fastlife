"""Inline templates."""

import inspect
from collections.abc import Callable
from typing import Any, ClassVar, get_args

from pydantic import BaseModel
from pydantic.config import ConfigDict

from fastlife.shared_utils.infer import is_union


class InlineTemplate(BaseModel):
    """
    Inline templates are used to encourage the location of behavior and the view typing.

    Pages produce templates that are not reusable and don't need to be reusable
    in there essence, they don't need to be in a component library.
    They use a component lirary to stay small but contains a view logic
    tighly coupled with the view and its code can stay in the same module of that view.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    template: ClassVar[str]
    """The template string to render."""
    renderer: ClassVar[str]
    """Template render engine to use."""


def is_inline_template_returned(endpoint: Callable[..., Any]) -> bool:
    signature = inspect.signature(endpoint)
    return_annotation = signature.return_annotation

    if isinstance(return_annotation, type) and issubclass(
        return_annotation, InlineTemplate
    ):
        return True

    if is_union(return_annotation):
        return any(
            isinstance(arg, type) and issubclass(arg, InlineTemplate)
            for arg in get_args(return_annotation)
        )

    return False
