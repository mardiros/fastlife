# Fastlife

[![Documentation](https://github.com/mardiros/fastlife/actions/workflows/publish-doc.yml/badge.svg)](https://mardiros.github.io/fastlife/)
[![Continuous Integration](https://github.com/mardiros/fastlife/actions/workflows/tests.yml/badge.svg)](https://github.com/mardiros/fastlife/actions/workflows/tests.yml)
[![Coverage Report](https://codecov.io/gh/mardiros/fastlife/graph/badge.svg?token=DTpi73d7mf)](https://codecov.io/gh/mardiros/fastlife)
[![Maintainability](https://api.codeclimate.com/v1/badges/94d107797b15b5e8843e/maintainability)](https://codeclimate.com/github/mardiros/fastlife/maintainability)

> ⚠️ **Under Heavy Development**
> Please note that this project is still in active development. Features and APIs may change frequently.
> Even the name is not definitive.

An opinionated Python web framework (based on {term}`FastAPI`).

## Purpose

Fastlife helps at building Web Application with session, security, html test client,
and html form generated from pydantic schema using customizable widget.

### Hypermedia based

In Fastlife, templates are made using {term}`XComponent`.
It's a modern HTML template made to create template with components.

Those components are currently stylized by {term}`Tailwind CSS`,
using [pytailwindcss](https://github.com/timonweb/pytailwindcss).

Even if it is not used by fastlife, it has been made to be used with {term}`HTMX`.

### First class configuration.

Fastlife is adding a "Configurator", like {term}`Pyramid` to get a better scallable codebase.

The configurator in fastlife organizes configuration settings hierarchically,
enabling easy management and overriding at different levels.
This promotes modularity and clarity in application configuration, making it simpler
to maintain and scale your project.

### Auto generated HTML Form.

Fastlife generate HTML Form from pydantic models, default widgets depending on
the type of the model's field but customizable to get the expected results.

It allows fast development of form to get early prototype to focus on what matter
the most.

### Tests

Fastlife comes with [a test client](https://mardiros.github.io/fastlife/develop/fastlife/fastlife.testing.testclient.html) that can interact with html inside unit tests.

### API

It also comes with an opinionated API wrapper made to enforce documentation consistency.
Under the wood, it's a FastAPI application made for writing API.

## Try it

The package is available on pypi with the name fastlifeweb.

```bash
pip install "fastlifeweb[xcomponent]"
```
