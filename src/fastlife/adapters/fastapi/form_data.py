"""
Set of functions to unserialize www-form-urlencoded format to python simple types.
"""

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import (
    Annotated,
    Any,
)

from fastapi import Depends

from fastlife.adapters.fastapi.request import Request


def unflatten_struct(
    flatten_input: Mapping[str, Any],
    unflattened_output: MutableMapping[str, Any] | MutableSequence[Any],
    level: int = 0,
    *,
    csrf_token_name: str | None = None,
) -> Mapping[str, Any] | Sequence[Any]:
    """
    Take a flatten_input map, with key segmented by `.` and build a nested dict.

    Fastlife use plain old web form to send data via HTTP POST, this function
    prepare the data before get injected to pydantic for serialization.
    """
    # we sort to ensure that list index are ordered
    # formkeys = sorted(flatten_input.keys())
    for key in flatten_input:
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
                unflattened_output.append(flatten_input[key])
            elif isinstance(unflattened_output, dict):
                unflattened_output[key] = flatten_input[key]
            else:
                raise TypeError(type(unflattened_output))
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
            raise TypeError(type(unflattened_output))

    return unflattened_output


async def unflatten_mapping_form_data(request: Request) -> Mapping[str, Any]:
    """
    Parse the {meth}`fastlife.request.request.form` and build a nested structure.
    """
    registry = request.registry
    form_data = await request.form()
    form_data_decode_list: MutableMapping[str, Any] = {}
    for key, val in form_data.multi_items():
        if key.endswith("[]"):
            key = key[:-2]
            if key not in form_data_decode_list:
                form_data_decode_list[key] = [val]
            else:
                form_data_decode_list[key].append(val)
        elif key in form_data_decode_list:
            if not isinstance(form_data_decode_list, list):
                form_data_decode_list[key] = [form_data_decode_list[key]]
            form_data_decode_list[key].append(val)
        else:
            form_data_decode_list[key] = val

    ret = unflatten_struct(
        form_data_decode_list, {}, csrf_token_name=registry.settings.csrf_token_name
    )  # type: ignore
    return ret  # type: ignore


async def unflatten_sequence_form_data(request: Request) -> Sequence[str]:
    """
    Parse the {meth}`fastlife.request.request.form` and build a list of structure.
    """
    registry = request.registry
    form_data = await request.form()
    # Could raise a value error !
    return unflatten_struct(  # type: ignore
        form_data, [], csrf_token_name=registry.settings.csrf_token_name
    )


MappingFormData = Annotated[Mapping[str, Any], Depends(unflatten_mapping_form_data)]
"""
Fast API Dependency to deserialize a {meth}`fastlife.request.request.Request.form`
to a dict.
"""
SequenceFormData = Annotated[Sequence[str], Depends(unflatten_sequence_form_data)]
"""
Fast API Dependency to deserialize a {meth}`fastlife.request.request.Request.form`
to a list.
"""
