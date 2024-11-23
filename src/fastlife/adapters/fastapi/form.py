"""HTTP Form serialization."""

from collections.abc import Callable, Mapping
from typing import Any

from fastapi import Depends

from fastlife.adapters.fastapi.form_data import MappingFormData
from fastlife.adapters.fastapi.request import Registry
from fastlife.domain.model.form import FormModel, T


def form_model(
    cls: type[T], name: str | None = None
) -> Callable[[Mapping[str, Any]], FormModel[T]]:
    """
    Build a model, a class of type T based on Pydandic Base Model from a form payload.
    """

    def to_model(data: MappingFormData, registry: Registry) -> FormModel[T]:
        prefix = name or registry.settings.form_data_model_prefix
        if not data:
            return FormModel[T].default(prefix, cls)
        return FormModel[T].from_payload(prefix, cls, data)

    return Depends(to_model)
