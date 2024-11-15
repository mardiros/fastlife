"""Inline templates."""

import inspect
from collections.abc import Callable
from typing import Any, get_args

from fastlife.domain.model.template import InlineTemplate
from fastlife.shared_utils.infer import is_union


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
