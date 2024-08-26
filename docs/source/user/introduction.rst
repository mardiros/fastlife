Introduction
============

Why building another framework ?

Well actually Fastlife is not really a framework, it's an overlay over FastAPI.

Currently, FastAPI is one of the best framework to build API, but can be used
to write classic website. It requires some code that you can write yourself or use
an overlay of the framework, like Fastlife.

I've personally and professionally use Pyramid for years, but, Python as evolve a lot,
especially the typing system, and Pyramid is not prepared for this update. I really
think it is true for all those framework created with Python 2 and migrated to
Python 3. By the way, some concept from Pyramid are used in Fastlife, especially for
dependecy injection at a lower level than what FastAPI provide.

The greatest strength of Fastlife is the form generation based on pydantic models.
Forms are created using widgets for each type, and can be overridden with a simple
annotation.

Fastlife use the JinjaX template engine, and comes with a set of JinjaX components
from basic html tag with htmx support to widgets for form generation.

Currently, Fastlife does not offer any tools for data storage.
