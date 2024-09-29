# Fastlife

[![Documentation](https://github.com/mardiros/fastlife/actions/workflows/gh-pages.yml/badge.svg)](https://mardiros.github.io/fastlife/)
[![Continuous Integration](https://github.com/mardiros/fastlife/actions/workflows/main.yml/badge.svg)](https://github.com/mardiros/fastlife/actions/workflows/main.yml)
[![Coverage Report](https://codecov.io/gh/mardiros/fastlife/graph/badge.svg?token=DTpi73d7mf)](https://codecov.io/gh/mardiros/fastlife)


> ⚠️ **Under Heavy Development**
> Please note that this project is still in active development. Features and APIs may change frequently.
> Even the name is not definitive.

An opinionated Python web framework (based on FastAPI).

## Purpose

Fastlife helps at building Web Application with session, security, html test client,
and html form generated from pydantic schema using customizable widget.

Templates are made using [JinjaX](https://jinjax.scaletti.dev/) and an extensible [set of
component](https://mardiros.github.io/fastlife/components/index.html) is available
in order to build pages.

Those components are currently stylized by [tailwindcss](https://tailwindcss.com/),
using [pytailwindcss](https://github.com/timonweb/pytailwindcss).

Moreover, you can also write API, in an opinionated way to enforce documentation
consistency.


## First class configuration.

Fastlife is adding a "Configurator", like Pyramid to get a better scallable codebase.

The configurator in fastlife organizes configuration settings hierarchically,
enabling easy management and overriding at different levels.
This promotes modularity and clarity in application configuration, making it simpler
to maintain and scale your project.


## Tests

Fastlife come with [a test client](https://mardiros.github.io/fastlife/develop/fastlife/fastlife.testing.testclient.html) that can interact with html inside unit tests.


## Try it

The package is available on pypi with the name fastlifeweb.

```bash
pip install fastlifeweb
```
