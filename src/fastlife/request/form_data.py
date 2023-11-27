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

from fastlife.configurator.registry import Registry


def unflatten_struct(
    flatten_input: Mapping[str, Any],
    unflattened_output: MutableMapping[str, Any] | MutableSequence[Any],
    level: int = 0,
    *,
    csrf_token_name: Optional[str] = None,
) -> Mapping[str, Any] | Sequence[Any]:
    # we sort to ensure that list index are ordered
    formkeys = sorted(flatten_input.keys())

    for key in formkeys:
        if csrf_token_name is not None and key == csrf_token_name:
            continue
        lkey, sep, rest = key.partition(".")

        if not sep:
            # this is a leaf
            if isinstance(unflattened_output, list):
                if not key.isdigit():
                    raise ValueError(f"{flatten_input}: Not a list")
                while int(key) != len(unflattened_output):
                    unflattened_output.append(None)
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
            while len(unflattened_output) < vkey:
                unflattened_output.append(None)
            if len(unflattened_output) < vkey + 1:
                sub_child_is_list = rest.partition(".")[0].isdigit()
                unflattened_output.append([] if sub_child_is_list else {})

            unflatten_struct(
                {rest: flatten_input[key]},
                unflattened_output[vkey],
                level + 1,
            )

        elif isinstance(unflattened_output, dict):
            if lkey not in unflattened_output:
                unflattened_output[lkey] = [] if child_is_list else {}
            unflatten_struct(
                {rest: flatten_input[key]},
                unflattened_output[lkey],
                level + 1,
            )
        else:
            raise ValueError(type(unflattened_output))

    return unflattened_output


async def unflatten_mapping_form_data(
    request: Request, reg: Registry
) -> Mapping[str, Any]:
    form_data = await request.form()
    ret = unflatten_struct(
        form_data, {}, csrf_token_name=reg.settings.csrf_token_name
    )  # type: ignore
    return ret  # type: ignore


async def unflatten_sequence_form_data(
    request: Request, reg: Registry
) -> Sequence[str]:
    form_data = await request.form()
    # Could raise a value error !
    return unflatten_struct(
        form_data, [], csrf_token_name=reg.settings.csrf_token_name
    )  # type: ignore


MappingFormData = Annotated[Mapping[str, Any], Depends(unflatten_mapping_form_data)]
SequenceFormData = Annotated[Sequence[str], Depends(unflatten_sequence_form_data)]


T = TypeVar("T", bound=BaseModel)
"""Template type for form serialized model"""


def model(cls: Type[T], name: Optional[str] = None) -> Callable[[Mapping[str, Any]], T]:
    """
    Build a model, a class of type T based on Pydandic Base Model from a form payload.
    """

    def to_model(data: MappingFormData, registry: Registry) -> Optional[T]:
        if data:
            return cls(**data[name or registry.settings.form_data_model_prefix])
        return None

    return Depends(to_model)
