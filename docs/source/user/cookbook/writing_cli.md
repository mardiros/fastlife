# Writing Command Line Interface

FastLife provides a built-in Command Line Interface (CLI) system designed for
development and maintenance tasks.

This implementation extends Typer's functionality while integrating with FastLife's
configuration system and dependency registry.

Key Features:

- Seamless integration with FastLife's registry.
- Asynchronous command support out of the box
- Configuration-driven CLI setup through FastLife's configurator.

The `AsyncTyper` class extends Typer to:

1. Automatically configure CLI applications using FastLife's settings
2. Enable native async command execution
3. Maintain compatibility with Typer's existing feature set

As for web routes, Fastlife configurator use venusian to inject CLI commands.

To inject CLI command, the decorator cli_command register the command in
a registry, the command hello_world is testable without modifification.

## Register cli command

```python
from fastlife.config.cli_command import cli_command


@cli_command(name="hello-world")
def hello_world() -> None:
    print("Hello World!")
```

To access to the registry add the registry argument to the function:

```python
from fastlife.config.cli_command import cli_command
from tests.fastlife_app.config import MyRegistry


@cli_command(name="print-user-id")
async def print_user_id(registry: MyRegistry, username: str):
    user = await registry.uow.users.get_user_by_username(username)
    print(user.user_id if user else "")
```

:::{tip}
Since Fastlife is made for async, the CLI can be async out of the box.
:::

## Build the CLI object

Example of how to build the cli object.

Imagine a package dummy, withthe module name `dummy.entrypoints.cli`

```python
from fastlife import Configurator, Settings
from fastlife.adapters.typer.cli import AsyncTyper


def build_cli() -> AsyncTyper:
    conf = Configurator(Settings())
    conf.include(".bin")
    return conf.build_cli()

main = build_cli()
```

The main Typer instance here has to be registered in the pyproject.toml in order
to let the python packaging build the final command.


```toml

[project.scripts]
my-dummy-command = "dummy.entrypoints.cli:main"

```

now, the command `my-dummy-command` is available.
