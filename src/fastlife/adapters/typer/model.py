"""Domain model of the typer integration."""

from collections.abc import Callable
from typing import Any

from typer.core import TyperCommand
from typer.models import CommandInfo, Default

CLIHook = Callable[..., Any]


class CLICommand:
    """Keep CLI command arguments and function for the final build."""

    hook: CLIHook
    cmd: CommandInfo

    def __init__(
        self,
        hook: CLIHook,
        name: str | None = None,
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
    ) -> None:
        self.hook = hook
        self.cmd = CommandInfo(
            name=name,
            cls=cls,
            context_settings=context_settings,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar or "[OPTIONS]",
            add_help_option=add_help_option,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
            rich_help_panel=rich_help_panel,
        )
