Getting Started
===============


First Steps
-----------

We can start with a simple hello world app, the fast api first step,
revisited.

hello world app
---------------

.. literalinclude:: examples/hello_world.py

In the example above, we can see that the FastAPI app has been encapsulated
inside a :class:`fastlife.config.configurator.Configurator` object.
The Configurator is responsible of the ASGI app construction, a FastAPI
app behind the scene.

.. note::

   If you have used the Pyramid framework, you are already familiar with its
   Configurator. Keep in mind that the Fastlife Configurator is a more naive
   implementation and less feature-rich.


The Configurator role, a builder pattern, is about reading settings, loading
routes, and configure an :class:`fastlife.config.registry.Registry`.

If you already build a FastAPI, or framework using route decoration, splitting
the routes in submodule requires some attention. Did you ever have circular
import problem ? The configurator solve those problems.

