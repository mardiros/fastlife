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
    get_origin,
)

from fastapi import Depends, Request
from pydantic import BaseModel, ValidationError
from result import Err, Ok, Result

from fastlife.configurator.registry import Registry
from fastlife.shared_utils.infer import is_union


def unflatten_struct(
    flatten_input: Mapping[str, Any],
    unflattened_output: MutableMapping[str, Any] | MutableSequence[Any],
    level: int = 0,
    *,
    csrf_token_name: Optional[str] = None,
) -> Mapping[str, Any] | Sequence[Any]:
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


async def unflatten_mapping_form_data(
    request: Request, reg: Registry
) -> Mapping[str, Any]:
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
        form_data_decode_list, {}, csrf_token_name=reg.settings.csrf_token_name
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
ModelResult = Result[T, Mapping[str, str]] | None


def model(
    cls: Type[T], name: str | None = None
) -> Callable[[Mapping[str, Any]], ModelResult[T]]:
    """
    Build a model, a class of type T based on Pydandic Base Model from a form payload.
    """

    def to_model(data: MappingFormData, registry: Registry) -> ModelResult[T]:
        if data:
            prefix = name or registry.settings.form_data_model_prefix
            try:
                return Ok(cls(**data[prefix]))
            except ValidationError as exc:
                errors: dict[str, str] = {}
                for error in exc.errors():
                    loc = prefix
                    typ: Any = cls
                    for part in error["loc"]:
                        if isinstance(part, str):
                            type_origin = get_origin(typ)
                            if type_origin:
                                if is_union(typ):
                                    args = typ.__args__
                                    for arg in args:
                                        if arg.__name__ == part:
                                            typ = arg
                                            continue

                                else:
                                    raise NotImplementedError
                            elif issubclass(typ, BaseModel):
                                typ = typ.model_fields[part].annotation
                                loc = f"{loc}.{part}"
                            else:
                                raise NotImplementedError

                        else:
                            # it is an integer and it part of the list
                            loc = f"{loc}.{part}"

                    if loc in errors:
                        errors[loc] = f"{errors[loc]}, {error['msg']}"
                    else:
                        errors[loc] = error["msg"]
                return Err(errors)
        return None

    return Depends(to_model)
