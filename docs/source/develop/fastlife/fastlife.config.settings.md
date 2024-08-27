# {py:mod}`fastlife.config.settings`

```{py:module} fastlife.config.settings
```

```{autodoc2-docstring} fastlife.config.settings
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Settings <fastlife.config.settings.Settings>`
  - ```{autodoc2-docstring} fastlife.config.settings.Settings
    :summary:
    ```
````

### API

`````{py:class} Settings(_case_sensitive: bool | None = None, _env_prefix: str | None = None, _env_file: pydantic_settings.sources.DotenvType | None = ENV_FILE_SENTINEL, _env_file_encoding: str | None = None, _env_ignore_empty: bool | None = None, _env_nested_delimiter: str | None = None, _env_parse_none_str: str | None = None, _env_parse_enums: bool | None = None, _cli_prog_name: str | None = None, _cli_parse_args: bool | list[str] | tuple[str, ...] | None = None, _cli_settings_source: pydantic_settings.sources.CliSettingsSource[typing.Any] | None = None, _cli_parse_none_str: str | None = None, _cli_hide_none_type: bool | None = None, _cli_avoid_json: bool | None = None, _cli_enforce_required: bool | None = None, _cli_use_class_docs_for_groups: bool | None = None, _cli_exit_on_error: bool | None = None, _cli_prefix: str | None = None, _secrets_dir: str | pathlib.Path | None = None, **values: typing.Any)
:canonical: fastlife.config.settings.Settings

Bases: {py:obj}`pydantic_settings.BaseSettings`

```{autodoc2-docstring} fastlife.config.settings.Settings
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.config.settings.Settings.__init__
```

````{py:attribute} model_config
:canonical: fastlife.config.settings.Settings.model_config
:value: >
   'SettingsConfigDict(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.model_config
```

````

````{py:attribute} fastlife_route_prefix
:canonical: fastlife.config.settings.Settings.fastlife_route_prefix
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.fastlife_route_prefix
```

````

````{py:attribute} template_search_path
:canonical: fastlife.config.settings.Settings.template_search_path
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.template_search_path
```

````

````{py:attribute} registry_class
:canonical: fastlife.config.settings.Settings.registry_class
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.registry_class
```

````

````{py:attribute} template_renderer_class
:canonical: fastlife.config.settings.Settings.template_renderer_class
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.template_renderer_class
```

````

````{py:attribute} form_data_model_prefix
:canonical: fastlife.config.settings.Settings.form_data_model_prefix
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.form_data_model_prefix
```

````

````{py:attribute} csrf_token_name
:canonical: fastlife.config.settings.Settings.csrf_token_name
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.csrf_token_name
```

````

````{py:attribute} jinjax_use_cache
:canonical: fastlife.config.settings.Settings.jinjax_use_cache
:type: bool
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.jinjax_use_cache
```

````

````{py:attribute} jinjax_auto_reload
:canonical: fastlife.config.settings.Settings.jinjax_auto_reload
:type: bool
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.jinjax_auto_reload
```

````

````{py:attribute} jinjax_global_catalog_class
:canonical: fastlife.config.settings.Settings.jinjax_global_catalog_class
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.jinjax_global_catalog_class
```

````

````{py:attribute} session_secret_key
:canonical: fastlife.config.settings.Settings.session_secret_key
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.session_secret_key
```

````

````{py:attribute} session_cookie_name
:canonical: fastlife.config.settings.Settings.session_cookie_name
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.session_cookie_name
```

````

````{py:attribute} session_cookie_domain
:canonical: fastlife.config.settings.Settings.session_cookie_domain
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.session_cookie_domain
```

````

````{py:attribute} session_cookie_path
:canonical: fastlife.config.settings.Settings.session_cookie_path
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.session_cookie_path
```

````

````{py:attribute} session_duration
:canonical: fastlife.config.settings.Settings.session_duration
:type: datetime.timedelta
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.session_duration
```

````

````{py:attribute} session_cookie_same_site
:canonical: fastlife.config.settings.Settings.session_cookie_same_site
:type: typing.Literal[lax, strict, none]
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.session_cookie_same_site
```

````

````{py:attribute} session_cookie_secure
:canonical: fastlife.config.settings.Settings.session_cookie_secure
:type: bool
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.session_cookie_secure
```

````

````{py:attribute} session_serializer
:canonical: fastlife.config.settings.Settings.session_serializer
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.session_serializer
```

````

````{py:attribute} domain_name
:canonical: fastlife.config.settings.Settings.domain_name
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.domain_name
```

````

````{py:attribute} check_permission
:canonical: fastlife.config.settings.Settings.check_permission
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.check_permission
```

````

````{py:attribute} decode_reverse_proxy_headers
:canonical: fastlife.config.settings.Settings.decode_reverse_proxy_headers
:type: bool
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.settings.Settings.decode_reverse_proxy_headers
```

````

`````
