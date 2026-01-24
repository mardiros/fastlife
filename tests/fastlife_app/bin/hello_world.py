from fastlife.config.cli_command import cli_command


@cli_command(name="hello-world")
def hello_world() -> None:
    print("Hello World!")
