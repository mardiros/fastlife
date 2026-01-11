"""HTTP Form serialization."""

from collections.abc import Mapping, Sequence
from typing import Annotated, Any, Generic, TypeVar, get_args, get_origin

from pydantic import BaseModel, ValidationError

from fastlife.shared_utils.infer import get_runtime_type, is_union

T = TypeVar("T", bound=BaseModel)
"""Template type for form serialized model"""


def get_type_by_discriminator(
    discriminant: str, discriminator: str, typ: type[Any]
) -> type[Any]:
    for child_typ in get_args(typ):
        if discriminant in child_typ.model_fields[discriminator].annotation.__args__:
            if get_origin(child_typ) is Annotated:
                child_typ = get_args(child_typ)[0]
            return child_typ
    raise ValueError(f"{discriminator} not found in {typ}")


def serialize_error(
    exc: ValidationError, prefix: str, pydantic_type: type[Any]
) -> dict[str, str]:
    errors: dict[str, str] = {}
    typ: Any = get_runtime_type(pydantic_type)
    for error in exc.errors():
        loc = prefix
        locations = iter(error["loc"])
        while True:
            part = next(locations, None)
            if part is None:
                break
            if isinstance(part, str):
                field = typ.model_fields[part]
                typ = field.annotation
                type_origin = get_origin(typ)
                if type_origin:
                    if is_union(typ):
                        loc = f"{loc}.{part}"
                        part = next(locations)
                        typ = get_type_by_discriminator(part, field.discriminator, typ)
                    else:
                        raise NotImplementedError from exc  # coverage: ignore
                elif issubclass(typ, BaseModel):
                    typ = typ.model_fields[part].annotation
                    loc = f"{loc}.{part}"
                else:
                    loc = f"{loc}.{part}"
                    break
            elif isinstance(part, int):
                # we are in a sequence
                loc = f"{loc}.{part}"
                assert isinstance(typ, Sequence)
                typ = typ.__args__[0]
            else:
                raise NotImplementedError from exc  # coverage: ignore

        if loc in errors:
            errors[loc] = f"{errors[loc]}, {error['msg']}"
        else:
            errors[loc] = error["msg"]
    return errors


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
            errors: dict[str, str] = serialize_error(exc, prefix, pydantic_type)
            # breakpoint()
            model = pydantic_type.model_construct(**data.get(prefix, {}))
            return cls(prefix, model, errors)
