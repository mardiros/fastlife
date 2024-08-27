# {py:mod}`fastlife.config.registry`

```{py:module} fastlife.config.registry
```

```{autodoc2-docstring} fastlife.config.registry
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`AppRegistry <fastlife.config.registry.AppRegistry>`
  - ```{autodoc2-docstring} fastlife.config.registry.AppRegistry
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_registry <fastlife.config.registry.get_registry>`
  - ```{autodoc2-docstring} fastlife.config.registry.get_registry
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Registry <fastlife.config.registry.Registry>`
  - ```{autodoc2-docstring} fastlife.config.registry.Registry
    :summary:
    ```
````

### API

`````{py:class} AppRegistry(settings: fastlife.config.settings.Settings)
:canonical: fastlife.config.registry.AppRegistry

```{autodoc2-docstring} fastlife.config.registry.AppRegistry
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.config.registry.AppRegistry.__init__
```

````{py:attribute} settings
:canonical: fastlife.config.registry.AppRegistry.settings
:type: fastlife.config.settings.Settings
:value: >
   None

```{autodoc2-docstring} fastlife.config.registry.AppRegistry.settings
```

````

````{py:attribute} renderer
:canonical: fastlife.config.registry.AppRegistry.renderer
:type: fastlife.templating.renderer.AbstractTemplateRendererFactory
:value: >
   None

```{autodoc2-docstring} fastlife.config.registry.AppRegistry.renderer
```

````

````{py:attribute} check_permission
:canonical: fastlife.config.registry.AppRegistry.check_permission
:type: fastlife.security.policy.CheckPermission
:value: >
   None

```{autodoc2-docstring} fastlife.config.registry.AppRegistry.check_permission
```

````

`````

````{py:function} get_registry(request: fastlife.request.request.Request) -> fastlife.config.registry.AppRegistry
:canonical: fastlife.config.registry.get_registry

```{autodoc2-docstring} fastlife.config.registry.get_registry
```
````

````{py:data} Registry
:canonical: fastlife.config.registry.Registry
:value: >
   None

```{autodoc2-docstring} fastlife.config.registry.Registry
```

````
