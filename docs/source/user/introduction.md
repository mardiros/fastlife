# Introduction

Welcome to the fastlife documentation!

Fastlife is a full-featured web framework based on the micro framework {term}`FastAPI`.

It provide features like html templates, web session, permissions, i18n, and
html form generation based on {term}`Pydantic` base models support out of the box.

Currently, FastAPI is one of the best micro framework. It can build be used
to build API with documentation almost for freen It can be used to write some
web pages. But to build more robust classic website, it lacks features that
you have to build on your own. Fastlife was created to fill this gap.

I've used Pyramid both personally and professionally for years,
but Python has evolved significantly, especially with its typing system,
and Pyramid isn't well-suited for this update.

Adding properties to requests isn't compatible with the typing system, and while
FastAPI's dependency injection is excellent for replacing that,
Pyramid's configurator offers much more.

Some concepts from Pyramid are utilized in Fastlife, particularly its configurator,
to bootstrap the application with dependency injection, which FastAPI doesn't provide.

Another great advantage of Fastlife is its form generation based on Pydantic models.

Forms are automatically created using widgets for each type, and can be easily
overridden with a simple annotation.

Fastlife use the JinjaX template engine, and comes with a set of JinjaX components
from basic html tag with htmx support to widgets for form generation.

Currently, Fastlife does not offer any tools for data storage.
