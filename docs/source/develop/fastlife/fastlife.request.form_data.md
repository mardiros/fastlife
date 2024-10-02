# {py:mod}`fastlife.request.form_data`

```{py:module} fastlife.request.form_data
```

```{autodoc2-docstring} fastlife.request.form_data
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`unflatten_mapping_form_data <fastlife.request.form_data.unflatten_mapping_form_data>`
  - ```{autodoc2-docstring} fastlife.request.form_data.unflatten_mapping_form_data
    :parser: myst
    :summary:
    ```
* - {py:obj}`unflatten_sequence_form_data <fastlife.request.form_data.unflatten_sequence_form_data>`
  - ```{autodoc2-docstring} fastlife.request.form_data.unflatten_sequence_form_data
    :parser: myst
    :summary:
    ```
* - {py:obj}`unflatten_struct <fastlife.request.form_data.unflatten_struct>`
  - ```{autodoc2-docstring} fastlife.request.form_data.unflatten_struct
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`MappingFormData <fastlife.request.form_data.MappingFormData>`
  - ```{autodoc2-docstring} fastlife.request.form_data.MappingFormData
    :parser: myst
    :summary:
    ```
* - {py:obj}`SequenceFormData <fastlife.request.form_data.SequenceFormData>`
  - ```{autodoc2-docstring} fastlife.request.form_data.SequenceFormData
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} MappingFormData
:canonical: fastlife.request.form_data.MappingFormData
:value: >
   None

```{autodoc2-docstring} fastlife.request.form_data.MappingFormData
:parser: myst
```

````

````{py:data} SequenceFormData
:canonical: fastlife.request.form_data.SequenceFormData
:value: >
   None

```{autodoc2-docstring} fastlife.request.form_data.SequenceFormData
:parser: myst
```

````

````{py:function} unflatten_mapping_form_data(request: fastlife.Request) -> typing.Mapping[str, typing.Any]
:canonical: fastlife.request.form_data.unflatten_mapping_form_data
:async:

```{autodoc2-docstring} fastlife.request.form_data.unflatten_mapping_form_data
:parser: myst
```
````

````{py:function} unflatten_sequence_form_data(request: fastlife.Request) -> typing.Sequence[str]
:canonical: fastlife.request.form_data.unflatten_sequence_form_data
:async:

```{autodoc2-docstring} fastlife.request.form_data.unflatten_sequence_form_data
:parser: myst
```
````

````{py:function} unflatten_struct(flatten_input: typing.Mapping[str, typing.Any], unflattened_output: typing.MutableMapping[str, typing.Any] | typing.MutableSequence[typing.Any], level: int = 0, *, csrf_token_name: typing.Optional[str] = None) -> typing.Mapping[str, typing.Any] | typing.Sequence[typing.Any]
:canonical: fastlife.request.form_data.unflatten_struct

```{autodoc2-docstring} fastlife.request.form_data.unflatten_struct
:parser: myst
```
````
