import inspect
from asyncio import run
from collections.abc import Callable
from functools import wraps
from typing import Any, Generic

from typer import Typer
from typer.core import DEFAULT_MARKUP_MODE, MarkupMode, TyperGroup
from typer.models import Default

from fastlife import TRegistry, TSettings
from fastlife.shared_utils.resolver import resolve

Command = Callable[..., Any]


class AsyncTyper(Typer, Generic[TSettings, TRegistry]):
    """
    An typer class made for fastlife application.

    Look at the Typer documentation for the details, this class inherits from it.
    """

    settings: TSettings
    """Access to settings."""

    registry: TRegistry
    """Access to the application registry."""

    def __init__(
        self,
        settings: TSettings,
        *,
        name: str | None = Default(None),
        cls: type[TyperGroup] | None = Default(None),  # noqa: B008
        invoke_without_command: bool = Default(False),
        no_args_is_help: bool = Default(False),
        subcommand_metavar: str | None = Default(None),
        chain: bool = Default(False),
        result_callback: Callable[..., Any] | None = Default(None),  # noqa: B008
        # Command
        context_settings: dict[Any, Any] | None = Default(None),  # noqa: B008
        callback: Callable[..., Any] | None = Default(None),  # noqa: B008
        help: str | None = Default(None),
        epilog: str | None = Default(None),
        short_help: str | None = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
        add_completion: bool = True,
        # Rich settings
        rich_markup_mode: MarkupMode = DEFAULT_MARKUP_MODE,
        rich_help_panel: str | None = Default(None),
        suggest_commands: bool = True,
        pretty_exceptions_enable: bool = True,
        pretty_exceptions_show_locals: bool = True,
        pretty_exceptions_short: bool = True,
    ):
        self.settings = settings
        registry_cls = resolve(settings.registry_class)
        self.registry = registry_cls(settings)
        super().__init__(
            name=name,
            cls=cls,
            invoke_without_command=invoke_without_command,
            no_args_is_help=no_args_is_help,
            subcommand_metavar=subcommand_metavar,
            chain=chain,
            result_callback=result_callback,
            context_settings=context_settings,
            callback=callback,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            hidden=hidden,
            deprecated=deprecated,
            add_completion=add_completion,
            rich_markup_mode=rich_markup_mode,
            rich_help_panel=rich_help_panel,
            suggest_commands=suggest_commands,
            pretty_exceptions_enable=pretty_exceptions_enable,
            pretty_exceptions_show_locals=pretty_exceptions_show_locals,
            pretty_exceptions_short=pretty_exceptions_short,
        )

    def command(self, *args: Any, **kwargs: Any) -> Command:
        """Override the Typer command to accept async functions."""

        def decorator(cmd: Command) -> Command:
            @wraps(cmd)
            def run_command(*cli_args: Any, **cli_kwargs: Any) -> Any:
                res = cmd(*cli_args, **cli_kwargs)
                if inspect.iscoroutine(res):
                    res = run(res)
                return res

            super(AsyncTyper, self).command(*args, **kwargs)(run_command)
            return cmd

        return decorator
