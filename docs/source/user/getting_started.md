# Getting Started

Today, there is a myriad of tools to start a Python project.

The `fastlifeweb` package can be installed from PyPI with your preferred virtualenv
manager.

## First Steps

We can start with a simple hello world app, the {term}`FastAPI` first step,
revisited.

## hello world app

```{literalinclude} examples/hello_world.py

```

In the example above, we can see that Fastlife build a FastAPI application.

In a classical {term}`FastAPI` application, the application is created an route, routers,
are added to it.
Using fastlife, the process has been reversed in a dependency injection process,
a {class}`Configurator <fastlife.config.configurator.Configurator>` object collect
all the routes, or any configuration like locale manager for i18n, and create
an app after everything has been collected.

The app build is a {term}`FastAPI` instance.

```{note}

   If you have used the Pyramid framework, you are already familiar with its
   Configurator. The Fastlife Configurator is a more naive implementation and
   less feature-rich.

```

The app can be started with the `fastapi dev` command or run with uvicorn asgi server.

```{code-block} bash
fastapi dev hello_world.py
```

## hello world app with a template

```{literalinclude} examples/hello_world_with_template.py

```

```{literalinclude} examples/templates/HelloWorld.jinja
:language: html
```

To use {term}`JinjaX` templates, templates path has to be registered using the
{meth}`Configurator.add_template_search_path <fastlife.config.configurator.Configurator.add_template_search_path>` or using
the settings {attr}`template_search_path <fastlife.config.settings.Settings.template_search_path>`.

Settings are {term}`pydantic settings`, it can be set from a environment variable prefixed by `fastlife_`.
You may also override the settings class to inject your own setting and override the prefix.

On the other hand, adding template search path during the configuration phase makes the app
more modular, and kept the module responsible of templates add its own template to the path.

```{note}
The most concerning can develop and register their own template engine using the
{meth}`fastlife.config.configurator.Configurator.add_renderer`.
```

## modular approach

A maintainable application over time is an application that encourage modularity.
In general, any application is divided into layers that have their own responsability.

The http views is one of them and now we are going split those views in a submodule.

Let's write a simple `views` module, with our previous view, and nothing more.

```{literalinclude} examples/modular/views.py
  :language: python
```

Now, we can use the {meth}`config.include() <fastlife.config.configurator.Configurator.include>`
method to inject routes in the final application.

```{literalinclude} examples/modular/entrypoint.py
  :language: python
```

The {meth}`config.include() <fastlife.config.configurator.Configurator.include>` call will
import the module **and all its submodules** and grab all decorated method with a
{func}`@configure <fastlife.config.configurator.configure>` afterwhat, the decorated method
will be called with the configurator as first argument in order to configure the module.

```{note}

  If you have used the Pyramid framework, the config.include does not works exactly the same.
  In Pyramid, there is no decorator on `includeme` function, and the include does not
  include submodule.
  In fastlife, `config.include()` works like if `config.scan()` will also call the includeme
  scanned.
  In Pyramid, the view and the route are not registered together, views are registered by
  a scan to set a view_name the the include attach the view name to routes in order to
  ensure that the routes are always registered in the same order.
  fastlife use a more traditional approach, and does not respect this strict approach,
  this is why the @view_config also register the path of the view.

```

## Writing tests

The {mod}`fastlife.testing.testclient` module define a set of class to help
writing test for web pages.

```{note}

  This module required the extra `testing` installable via the command

  ```bash
  pip install fastlifeweb[testing]

```



```{literalinclude} examples/modular/test_views.py
  :language: python
```
