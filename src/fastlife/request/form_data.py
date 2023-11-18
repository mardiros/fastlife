from typing import (
    Annotated,
    Any,
    Callable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

from fastapi import Depends, Request
from pydantic import BaseModel

from fastlife.security.csrf import CSRF_TOKEN_NAME


def unflatten_struct(
    flatten_input: Mapping[str, Any],
    unflattened_output: MutableMapping[str, Any] | MutableSequence[Any],
    level: int = 0,
) -> Mapping[str, Any] | Sequence[Any]:
    # we sort to ensure that list index are ordered
    formkeys = sorted(flatten_input.keys())

    for key in formkeys:
        if key == CSRF_TOKEN_NAME and level == 0:
            continue
        lkey, sep, rest = key.partition(".")

        if not sep:
            # this is a leaf
            if isinstance(unflattened_output, list):
                if not key.isdigit():
                    raise ValueError(f"{flatten_input}: Not a list")
                if not int(key) == len(unflattened_output):
                    raise ValueError(
                        f"{flatten_input}: Missing index {len(unflattened_output)}"
                    )
                unflattened_output.append(flatten_input[key])
            elif isinstance(unflattened_output, dict):
                unflattened_output[key] = flatten_input[key]
            else:
                raise ValueError(type(unflattened_output))
            continue

        child_is_list = rest.partition(".")[0].isdigit()
        if isinstance(unflattened_output, list):
            vkey = int(lkey)
            if len(unflattened_output) < vkey + 1:
                sub_child_is_list = rest.partition(".")[0].isdigit()
                unflattened_output.append([] if sub_child_is_list else {})

            unflatten_struct(
                {rest: flatten_input[key]}, unflattened_output[vkey], level + 1
            )

        elif isinstance(unflattened_output, dict):
            if lkey not in unflattened_output:
                unflattened_output[lkey] = [] if child_is_list else {}
            unflatten_struct(
                {rest: flatten_input[key]}, unflattened_output[lkey], level + 1
            )
        else:
            raise ValueError(type(unflattened_output))

    return unflattened_output


async def unflatten_mapping_form_data(request: Request) -> Mapping[str, Any]:
    form_data = await request.form()
    return unflatten_struct(form_data, {})  # type: ignore


async def unflatten_sequence_form_data(request: Request) -> Sequence[str]:
    form_data = await request.form()
    # Could raise a value error !
    return unflatten_struct(form_data, [])  # type: ignore


MappingFormData = Annotated[Mapping[str, Any], Depends(unflatten_mapping_form_data)]
SequenceFormData = Annotated[Sequence[str], Depends(unflatten_sequence_form_data)]


T = TypeVar("T", bound=BaseModel)


def FormModel(cls: Type[T]) -> Callable[[Mapping[str, Any]], T]:
    def form_model(data: MappingFormData) -> T:
        return cls(**data)

    return Depends(form_model)


def OptionalFormModel(cls: Type[T]) -> Callable[[Mapping[str, Any]], T]:
    def form_model(data: MappingFormData) -> Optional[T]:
        if data:
            return cls(**data["payload"])
        return None

    return Depends(form_model)
