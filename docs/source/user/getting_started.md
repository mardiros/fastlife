# Getting Started

## Installation

Today, there is a myriad of tools to start a Python project.

The `fastlifeweb` package can be installed from PyPI with your preferred virtualenv
manager.

```{note}
This section does not explain how to package an application, it explain the philosophy
of the framewoks compare to other frameworks such has {term}`Pyramid` and
{term}`FastAPI` to get started fast.

The cookook has recipes to build properly packaged application using poetry.
```

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
a {class}`Configurator <fastlife.config.configurator.GenericConfigurator>` object collect
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

```{important}
This documentation use the old/deprecated template engine JinjaX, and has to be rewritten.
```


```{literalinclude} examples/hello_world_with_template.py

```

The template is included inline, for many reasons.

The first one is to encourage the principle of {term}`locality of behavior`, instead of
the "separation of concern".

The second reason is that it encore typing. While inlining template in the code,
we can add parameters to the returned object too, an instance of a
{class}`fastlife.XTemplate` is a self complete object
ready to be rendered.

Don't be afraid, we have written html node here, for the introduction, but,
it is also encouraged to build a set of library component with pure template,
such as a Layout component to set the template to somethinf like
`<Layout>Hello World</Layout>`.

## modular approach

A maintainable application over time is an application that encourage modularity.
In general, any application is divided into layers that have their own responsability.

The http views is one of them and now we are going split those views in a submodule.

Let's write a simple `views` module, with our previous view, and nothing more.

```{literalinclude} examples/modular/views.py
  :language: python
```

We have a library of component, created directly in the same directory for simplicity.

```{literalinclude} examples/modular/Layout.jinja
  :language: html
```

And now, we can use the
{meth}`config.include() <fastlife.config.configurator.GenericConfigurator.include>`
method to inject routes in the final application.

```{literalinclude} examples/modular/entrypoint.py
  :language: python
```

The {meth}`config.include() <fastlife.config.configurator.GenericConfigurator.include>` call will
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

````{note}

  This module required the extra `testing` installable via the command.

  ```bash
  pip install fastlifeweb[testing]

````

```{literalinclude} examples/modular/test_views.py
  :language: python
```
