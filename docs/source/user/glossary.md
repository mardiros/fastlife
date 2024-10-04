# Glossary

```{glossary}
```

[FastAPI](https://fastapi.tiangolo.com/)
: FastAPI is micro frameword based on ASGI.

[Jinjax](https://jinjax.scaletti.dev/)
: JinjaX is a template engine for made for clarity.
It is an extension of the Jinja2 template engine.

[OpenAPI](https://www.openapis.org/)
: OpenAPI is a specification for building APIs that defines a standard way to describe
the structure and capabilities of RESTful APIs in a machine-readable format.
FastAPI generates the OpenAPI spec file directly from its API.

[Redoc](https://redocly.com/docs/redoc)
: An alternative to Swagger UI. An interactive documentation from Open API Format.

[Swagger UI](https://swagger.io/tools/swagger-ui/)
: Swagger UI is a web interface that create a documentation and a playground to test
API based on the Open API format.

[Pyramid](https://trypyramid.com/)
: Pyramid is Python Web Framework based on WSGI.
fastlife take a lots of inspiration from Pyramid.

[Pydantic](https://docs.pydantic.dev/latest/)
: Pydantic is a widely used Python library
for data validation. Pydantic ensures your data is accurate and well-structured
by validating it as you work with Python classes.
In Fastlife, Pydantic models are also used to generate HTML form models using
a set of extensible {mod}`fastlife.adapters.jinjax.widgets`.

[Pydantic Settings](https://docs.pydantic.dev/latest/api/pydantic_settings/)
: Pydantic Settings is a library made to load your setting from multiple source.
Environment variables is encouraged by the library.
