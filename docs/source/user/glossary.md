# Glossary


```{glossary}

FastAPI
  FastAPI is micro frameword based on ASGI.

  Website: https://fastapi.tiangolo.com/

HTMX
  HTMX is a javascript library that extend HTML to do
  [https://htmx.org/essays/hypermedia-driven-applications/](hypermedia driven applications).
  Fastlife is a web framework made for this kind of architecture arround HTMX.

  Website: https://htmx.org/

Jinjax
  JinjaX is a template engine for made for clarity.
  It is an extension of the Jinja2 template engine.

  Website: https://jinjax.scaletti.dev/

Locality Of Behavior
  An HTMX, or Hypermedia driven application principle that says:

  > The behaviour of a unit of code should be as obvious as possible by looking
  > only at that unit of code

  Website: https://htmx.org/essays/locality-of-behaviour/

OpenAPI
  OpenAPI is a specification for building APIs that defines a standard way to describe
  the structure and capabilities of RESTful APIs in a machine-readable format.
  FastAPI generates the OpenAPI spec file directly from its API.

  Website: https://www.openapis.org/


Pyramid
  Pyramid is Python Web Framework based on WSGI.
  fastlife take a lots of inspiration from Pyramid.

  Website: https://trypyramid.com/


Pydantic
  Pydantic is a widely used Python library for data validation.

  Pydantic ensures your data is accurate and well-structured by validating it as you
  work with Python classes.

  In Fastlife, Pydantic models are also used to generate HTML form models using
  a set of extensible {mod}`fastlife.adapters.jinjax.widgets`.

  Website: https://docs.pydantic.dev/latest/


Pydantic Settings
  Pydantic Settings is a library made to load your setting from multiple source.
  Environment variables is encouraged by the library.

  Website: https://docs.pydantic.dev/latest/api/pydantic_settings/


Redoc
  An alternative to Swagger UI. An interactive documentation from {term}`OpenAPI` Format.

  Website: https://redocly.com/docs/redoc


Swagger UI
  Swagger UI is a web interface that create a documentation and a playground to test
  API based on the {term}`OpenAPI` format.

  Website: https://swagger.io/tools/swagger-ui/


Tailwind CSS
  A CSS framework where you compose with existing class intead of writings your own ones.

  Website: https://tailwindcss.com/docs/

Widget
  A widget in fastlife refer to a {term}`JinjaX` compoment made for handling data input
  in a form for a {term}`Pydantic` field.
```
