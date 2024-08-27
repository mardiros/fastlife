# {py:mod}`fastlife.templating.renderer.widgets.factory`

```{py:module} fastlife.templating.renderer.widgets.factory
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`WidgetFactory <fastlife.templating.renderer.widgets.factory.WidgetFactory>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory
    :summary:
    ```
````

### API

`````{py:class} WidgetFactory(renderer: fastlife.templating.renderer.abstract.AbstractTemplateRenderer, token: typing.Optional[str] = None)
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.__init__
```

````{py:method} get_markup(model: fastlife.request.form.FormModel[typing.Any], *, removable: bool = False, field: pydantic.fields.FieldInfo | None = None) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.get_markup

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.get_markup
```

````

````{py:method} get_widget(base: typing.Type[typing.Any], form_data: typing.Mapping[str, typing.Any], form_errors: typing.Mapping[str, typing.Any], *, prefix: str, removable: bool, field: pydantic.fields.FieldInfo | None = None) -> fastlife.templating.renderer.widgets.base.Widget[typing.Any]
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.get_widget

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.get_widget
```

````

````{py:method} build(typ: typing.Type[typing.Any], *, name: str = '', value: typing.Any, removable: bool, form_errors: typing.Mapping[str, typing.Any], field: pydantic.fields.FieldInfo | None = None) -> fastlife.templating.renderer.widgets.base.Widget[typing.Any]
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.build

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.build
```

````

````{py:method} build_model(field_name: str, typ: typing.Type[pydantic.BaseModel], field: typing.Optional[pydantic.fields.FieldInfo], value: typing.Mapping[str, typing.Any], form_errors: typing.Mapping[str, typing.Any], removable: bool) -> fastlife.templating.renderer.widgets.base.Widget[typing.Any]
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.build_model

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.build_model
```

````

````{py:method} build_union(field_name: str, field_type: typing.Type[typing.Any], field: typing.Optional[pydantic.fields.FieldInfo], value: typing.Any, form_errors: typing.Mapping[str, typing.Any], removable: bool) -> fastlife.templating.renderer.widgets.base.Widget[typing.Any]
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.build_union

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.build_union
```

````

````{py:method} build_sequence(field_name: str, field_type: typing.Type[typing.Any], field: typing.Optional[pydantic.fields.FieldInfo], value: typing.Optional[collections.abc.Sequence[typing.Any]], form_errors: typing.Mapping[str, typing.Any], removable: bool) -> fastlife.templating.renderer.widgets.base.Widget[typing.Any]
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.build_sequence

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.build_sequence
```

````

````{py:method} build_set(field_name: str, field_type: typing.Type[typing.Any], field: typing.Optional[pydantic.fields.FieldInfo], value: typing.Optional[collections.abc.Sequence[typing.Any]], form_errors: typing.Mapping[str, typing.Any], removable: bool) -> fastlife.templating.renderer.widgets.base.Widget[typing.Any]
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.build_set

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.build_set
```

````

````{py:method} build_boolean(field_name: str, field_type: typing.Type[typing.Any], field: pydantic.fields.FieldInfo | None, value: bool, form_errors: typing.Mapping[str, typing.Any], removable: bool) -> fastlife.templating.renderer.widgets.base.Widget[typing.Any]
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.build_boolean

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.build_boolean
```

````

````{py:method} build_emailtype(field_name: str, field_type: typing.Type[typing.Any], field: pydantic.fields.FieldInfo | None, value: str | int | float, form_errors: typing.Mapping[str, typing.Any], removable: bool) -> fastlife.templating.renderer.widgets.base.Widget[typing.Any]
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.build_emailtype

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.build_emailtype
```

````

````{py:method} build_secretstr(field_name: str, field_type: typing.Type[typing.Any], field: pydantic.fields.FieldInfo | None, value: pydantic.SecretStr | str, form_errors: typing.Mapping[str, typing.Any], removable: bool) -> fastlife.templating.renderer.widgets.base.Widget[typing.Any]
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.build_secretstr

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.build_secretstr
```

````

````{py:method} build_literal(field_name: str, field_type: typing.Type[typing.Any], field: pydantic.fields.FieldInfo | None, value: str | int | float, form_errors: typing.Mapping[str, typing.Any], removable: bool) -> fastlife.templating.renderer.widgets.base.Widget[typing.Any]
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.build_literal

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.build_literal
```

````

````{py:method} build_enum(field_name: str, field_type: typing.Type[typing.Any], field: pydantic.fields.FieldInfo | None, value: str | int | float, form_errors: typing.Mapping[str, typing.Any], removable: bool) -> fastlife.templating.renderer.widgets.base.Widget[typing.Any]
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.build_enum

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.build_enum
```

````

````{py:method} build_simpletype(field_name: str, field_type: typing.Type[typing.Any], field: pydantic.fields.FieldInfo | None, value: str | int | float, form_errors: typing.Mapping[str, typing.Any], removable: bool) -> fastlife.templating.renderer.widgets.base.Widget[typing.Any]
:canonical: fastlife.templating.renderer.widgets.factory.WidgetFactory.build_simpletype

```{autodoc2-docstring} fastlife.templating.renderer.widgets.factory.WidgetFactory.build_simpletype
```

````

`````
