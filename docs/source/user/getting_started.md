# Getting Started

## First Steps

We can start with a simple hello world app, the fast api first step,
revisited.

## hello world app

```{literalinclude} examples/hello_world.py

```

In the example above, we can see that the FastAPI app has been encapsulated
inside a :class:`fastlife.config.configurator.Configurator` object.
The Configurator is responsible of the ASGI app construction, a FastAPI
app behind the scene.

```{note}

   If you have used the Pyramid framework, you are already familiar with its
   Configurator. The Fastlife Configurator is a more naive implementation and
   less feature-rich.

```

You can start the app using fastapi dev command.

```{code-block} bash
fastapi dev hello_world.py
```

The Configurator role, a builder pattern, is about reading settings, loading
routes, and configure an :class:`fastlife.config.registry.Registry`.

If you have already built a FastAPI application or a framework using route decorators,
splitting the routes into submodules requires careful handling to avoid issues.
Have you ever encountered circular import problems?
The configurator helps solve these issues.

With Fastlife, you never use a global app object,
which helps prevent circular dependencies.

Instead, The application is build using the
{method}`Configurator.build_asgi_app() <fastlife.config.configurator.Configurator.build_asgi_app>`.

This entry point provides access to HTTP routes without being the application directly.


## modular approach

A maintainable application over time is an application that encourage modularity.
In general, any application is divided into layers that have their own responsability.

The http views is one of them and now we are going split those views in a submodule.

Let's write a simple `views` module, with our previous view, and nothing more.

```{literalinclude} examples/modular/views.sh
  :language: python
  :emphasize-lines: 9
```

Now, we can use the {meth}`config.include() <fastlife.config.configurator.Configurator.include>`
method to inject routes in the final application.

```{literalinclude} examples/modular/entrypoint.sh
  :language: python
  :emphasize-lines: 6
```

The {meth}`config.include() <fastlife.config.configurator.Configurator.include>` call will
import the module **and all its submodules** and grab all decorated method with a
{func}`@configure <fastlife.config.configurator.configure>` afterwhat, the decorated method
will be called with the configurator as an argument in order to configure the module.

```{note}

  If you have used the Pyramid framework, the config.include does not works exactly the same.
  In pyramid, there is no decorator on `includeme` function, and the include does not
  include submodule.
  In fastlife, `config.include()` works like if `config.scan()` will also call the includeme
  scanned.
```

You can start the app using fastapi dev command.

```{code-block} bash
fastapi dev entrypoint.py
```

## HTML Response with templates.

We can rewrite our `views` module now and use an html template tor the response.

```{literalinclude} examples/modular/views_with_template.sh
  :language: python
  :emphasize-lines: 8,10
```

Fastlife use [JinjaX](https://jinjax.scaletti.dev/) template engine, a modern and
modular template engine. lets write a simple template.

```{literalinclude} examples/modular/HelloWorld.jinja.sh
  :language: bash
```

Now to run our app, we need to add a settings to find the templates.

```{code-block} bash
FASTLIFE_TEMPLATE_SEARCH_PATH=. poetry run fastapi dev entrypoint.py
```
