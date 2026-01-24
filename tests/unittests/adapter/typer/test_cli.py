from typer.testing import CliRunner

from fastlife.adapters.typer.cli import AsyncTyper
from tests.fastlife_app.config import MyRegistry, MySettings

dummycli = AsyncTyper[MyRegistry](MyRegistry(MySettings()), name="dummycli")


@dummycli.command(name="print-user-id")
async def print_user_id(username: str):
    user = await dummycli.registry.uow.users.get_user_by_username(username)
    print(user.user_id if user else "")


def test_cli():
    runner = CliRunner()
    result = runner.invoke(dummycli, ["Bob"])
    assert result.exit_code == 0
    assert result.stdout == "00000000-0000-0000-0000-000000000001\n"
