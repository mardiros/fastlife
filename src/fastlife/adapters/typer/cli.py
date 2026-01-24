"""
CLI Application Integration
"""

import inspect
from asyncio import run
from collections.abc import Callable
from functools import wraps
from typing import Any, Generic

from typer import Typer
from typer.core import DEFAULT_MARKUP_MODE, MarkupMode, TyperCommand, TyperGroup
from typer.models import Default

from fastlife import TRegistry
from fastlife.adapters.typer.model import CLIHook


class AsyncTyper(Typer, Generic[TRegistry]):
    """
    An typer class made for fastlife application.

    Look at the Typer documentation for the details, this class inherits from it.
    """

    registry: TRegistry
    """Access to the application registry."""

    def __init__(
        self,
        registry: TRegistry,
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
        self.registry = registry
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

    def command(
        self,
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
        """Override the Typer command to accept async functions."""

        def decorator(cmd: CLIHook) -> CLIHook:
            # Get the original command signature
            sig = inspect.signature(cmd)
            # Remove the registry parameter from the signature
            has_registry = False
            new_params: list[inspect.Parameter] = []
            for param_name, param in sig.parameters.items():
                if param_name == "registry":
                    has_registry = True
                else:
                    new_params.append(param)

            def build_signature(
                original_func: Callable[..., Any], new_params: list[inspect.Parameter]
            ) -> inspect.Signature:
                """
                Create a new signature for the wrapped function for typer.

                We remove the registry if exists and then
                """
                return inspect.Signature(
                    parameters=new_params,
                    return_annotation=original_func.__annotations__.get("return"),
                )

            @wraps(
                cmd,
                assigned=(
                    "__module__",
                    "__name__",
                    "__qualname__",
                    "__doc__",
                    "__annotations__",
                ),
            )
            def run_command(**cli_kwargs: Any) -> Any:
                if has_registry:
                    cli_kwargs["registry"] = self.registry
                res = cmd(**cli_kwargs)
                if inspect.iscoroutine(res):
                    res = run(res)
                return res

            run_command.__signature__ = build_signature(  # type: ignore
                cmd, new_params
            )

            super(AsyncTyper, self).command(
                name=name,
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
            )(run_command)
            return cmd

        return decorator
