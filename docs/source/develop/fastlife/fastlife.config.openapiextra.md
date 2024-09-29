# {py:mod}`fastlife.config.openapiextra`

```{py:module} fastlife.config.openapiextra
```

```{autodoc2-docstring} fastlife.config.openapiextra
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`ExternalDocs <fastlife.config.openapiextra.ExternalDocs>`
  - ```{autodoc2-docstring} fastlife.config.openapiextra.ExternalDocs
    :parser: myst
    :summary:
    ```
* - {py:obj}`OpenApiTag <fastlife.config.openapiextra.OpenApiTag>`
  - ```{autodoc2-docstring} fastlife.config.openapiextra.OpenApiTag
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} ExternalDocs(/, **data: typing.Any)
:canonical: fastlife.config.openapiextra.ExternalDocs

Bases: {py:obj}`pydantic.BaseModel`

```{autodoc2-docstring} fastlife.config.openapiextra.ExternalDocs
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.config.openapiextra.ExternalDocs.__init__
:parser: myst
```

````{py:attribute} description
:canonical: fastlife.config.openapiextra.ExternalDocs.description
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.config.openapiextra.ExternalDocs.description
:parser: myst
```

````

````{py:attribute} url
:canonical: fastlife.config.openapiextra.ExternalDocs.url
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.config.openapiextra.ExternalDocs.url
:parser: myst
```

````

`````

`````{py:class} OpenApiTag(/, **data: typing.Any)
:canonical: fastlife.config.openapiextra.OpenApiTag

Bases: {py:obj}`pydantic.BaseModel`

```{autodoc2-docstring} fastlife.config.openapiextra.OpenApiTag
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.config.openapiextra.OpenApiTag.__init__
:parser: myst
```

````{py:attribute} description
:canonical: fastlife.config.openapiextra.OpenApiTag.description
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.config.openapiextra.OpenApiTag.description
:parser: myst
```

````

````{py:attribute} external_docs
:canonical: fastlife.config.openapiextra.OpenApiTag.external_docs
:type: fastlife.config.openapiextra.ExternalDocs | None
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.openapiextra.OpenApiTag.external_docs
:parser: myst
```

````

````{py:attribute} name
:canonical: fastlife.config.openapiextra.OpenApiTag.name
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.config.openapiextra.OpenApiTag.name
:parser: myst
```

````

`````
