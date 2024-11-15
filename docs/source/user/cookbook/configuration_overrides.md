# Overriding configuration

Configuring an application depends of the app itself and storage backends.

At the moment, fastlife does not offers a way to works with any storage backend.

But the {class}`Configurator <fastlife.config.Configurator>` has been designed to
be extensible, so this section will explain how to add your own settings
and configure your own services in the registry.

## Adding new settings

To add your own settings, the Settings class has to be overriden.
In the folowwing example we will override the settings to:

- change the env var prefix to get application related one.
- add a setting 'unit_of_work' that will implement be used to register
  an implementation.

```python
from fastlife import Settings


class MySettings(Settings):
    model_config = SettingsConfigDict(env_prefix="myapp_", case_sensitive=False)
    unit_of_work: str = Field(
        default="myapp.adapters.inmemory_uow:InMemoryUnitOfWork",
    )
    database_url: str | None = Field(
        default=None, description="URL of the database if the SQLUnitOfWork is used"
    )

    # override the settings to register our own registry.
    registry_class: str = "myapp.config:MyRegistry"
    """Implementation class for the application regitry."""

```

Here we supposed that the application has been packaged under the name `myapp`,
and there is a class `InMemoryUnitOfWork` in the module `myapp.adapters.inmemory_uow`.
The `database_url` is used for the SQL version of the unit of work.

We are not coverring that in this cookbook, we are focusing on how to add
a dependency injection in your own application.

In the settings there is spcial settings name `registry_class` that is a dependency
injection of the registry available in all requests. By specifying it, this one
will replace the {class}`default registry <fastlife.config.registry.DefaultRegistry>`.

Now we have to implment our own registry and resolve our dependency injection.

## Adding the specific registry.

In the previous section, we've specified a `registry_class` and now it's time
to implement it.

```python
from fastlife import GenericRegistry
from fastlife.shared_utils.resolver import resolve
from myapp.service.uow import AbstractUnitOfWork

... # previous code redacted

class MyRegistry(GenericRegistry[MySettings]):
    uow: AbstractUnitOfWork

    def __init__(self, settings: MySettings) -> None:
        super().__init__(settings)
        self.uow = resolve(settings.uow)(settings)

```

To convert a string to an implementation, the
{func}`resolve <fastlife.shared_utils.resolver import resolve>` is used to
get class, and we passed the settings in parameter of the constructor in order
to initialized it.
This way, the implementation access its own settings saved in the registry settings.

## Finalize our typing

The {class}`Request <fastlife.request.request.Request>` and the
{class}`Configurator <fastlife.config.configurator.GenericConfigurator>` types are
expecting the {class}`DefaultRegistry <fastlife.config.registry.DefaultRegistry>`
to be used, and now we have additionnal properties, so, in order to finalize it,
we need to build our own request and configurator type.

```python
from fastlife import GenericConfigurator, GenericRegistry, Settings, DefaultRegistry
from fastlife.request import GenericRequest, get_request

... # previous code redacted

MyConfigurator = GenericConfigurator[MyRegistry]
MyRequest = Annotated[GenericRequest[MyRegistry], Depends(get_request)]
```

That's it!

Now, you can use `MyConfigurator` as a configurator, and if you want
to inject your own methods consumed in your
{meth}`@configure <fastlife.config.configurator.configure>`, fill free!

The `MyRequest` is a FastAPI dependency injection that is properly type
for all your views that have access to the registry.

```python
from fastlife import Response


... # previous code redacted


def my_view(request: MyRequest):
    return Response("Ok")


def build_app():
    conf = MyConfigurator(MySettings())
    conf.add_route("my_view", "/", my_view)
    return conf.build_asgi_app()


app = build_app()

```
