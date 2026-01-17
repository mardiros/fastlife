"""HTTP Form serialization."""

from collections.abc import Mapping
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ValidationError

from fastlife.shared_utils.form import flatten_error

T = TypeVar("T", bound=BaseModel)
"""Template type for form serialized model"""


class FormModel(Generic[T]):
    prefix: str
    model: T
    fatal_error: str
    errors: dict[str, str]
    is_valid: bool

    def __init__(
        self, prefix: str, model: T, errors: dict[str, Any], is_valid: bool = False
    ) -> None:
        self.prefix = prefix
        self.model = model
        self.fatal_error = ""
        self.errors = errors
        self.is_valid = is_valid

    @classmethod
    def default(cls, prefix: str, pydantic_type: type[T]) -> "FormModel[T]":
        return cls(prefix, pydantic_type.model_construct(), {})

    def set_fatal_error(self, value: str) -> None:
        self.fatal_error = value
        self.is_valid = False

    def add_error(self, field: str, value: str) -> None:
        self.errors[f"{self.prefix}.{field}"] = value
        self.is_valid = False

    def edit(self, pydantic_type: T) -> None:
        """
        Load the form with the given model and consider it as valid for the user.

        No error will be reported.
        """
        self.model = pydantic_type
        self.errors = {}
        self.is_valid = True

    @property
    def form_data(self) -> Mapping[str, Any]:
        return {self.prefix: self.model.model_dump(warnings="none")}

    @classmethod
    def from_payload(
        cls, prefix: str, pydantic_type: type[T], data: Mapping[str, Any]
    ) -> "FormModel[T]":
        try:
            ptyp = pydantic_type(**data.get(prefix, {}))
            ret = cls(prefix, ptyp, {}, True)
            return ret
        except ValidationError as exc:
            errors: dict[str, str] = flatten_error(exc, prefix, pydantic_type)
            model = pydantic_type.model_construct(**data.get(prefix, {}))
            return cls(prefix, model, errors)
