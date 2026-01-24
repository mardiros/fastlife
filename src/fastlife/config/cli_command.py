"""
Configure views using a decorator.

A simple usage:

```python
from typing import Annotated

from fastapi import Response
from fastlife import Template, template, view_config


@view_config("hello_world", "/", methods=["GET"])
async def hello_world(
    template: Annotated[Template, template("HelloWorld.jinja")],
) -> Response:
    return template()
```
"""

from typing import Any

import venusian
from typer.core import TyperCommand
from typer.models import Default

from fastlife.adapters.typer.model import CLICommand, CLIHook

from .configurator import VENUSIAN_CATEGORY, Configurator


def cli_command(
    name: str | None = None,
    *,
    cls: type[TyperCommand] | None = None,
    context_settings: dict[Any, Any] | None = None,
    help: str | None = None,
    epilog: str | None = None,
    short_help: str | None = None,
    options_metavar: str | None = None,
    add_help_option: bool = True,
    no_args_is_help: bool = False,
    hidden: bool = False,
    deprecated: bool = False,
    rich_help_panel: str | None = Default(None),
) -> CLIHook:
    """
    A decorator function to register a websocket view in the
    {class}`Configurator <fastlife.config.configurator.GenericConfigurator>`
    while scaning a module using {func}`include
    <fastlife.config.configurator.GenericConfigurator.include>`.

    :return: the configuration callback.
    """
    command_name = name

    def configure(
        wrapped: CLIHook,
    ) -> CLIHook:
        def callback(scanner: venusian.Scanner, name: str, ob: CLIHook) -> None:
            if not hasattr(scanner, VENUSIAN_CATEGORY):
                return  # coverage: ignore
            config: Configurator = getattr(scanner, VENUSIAN_CATEGORY)
            config.add_cli_command(
                CLICommand(
                    hook=wrapped,
                    name=command_name,
                    cls=cls,
                    context_settings=context_settings,
                    help=help,
                    epilog=epilog,
                    short_help=short_help,
                    options_metavar=options_metavar,
                    add_help_option=add_help_option,
                    no_args_is_help=no_args_is_help,
                    hidden=hidden,
                    deprecated=deprecated,
                    rich_help_panel=rich_help_panel,
                )
            )

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
        return wrapped

    return configure
