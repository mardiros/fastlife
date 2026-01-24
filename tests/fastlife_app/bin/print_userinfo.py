from fastlife.config.cli_command import cli_command
from tests.fastlife_app.config import MyRegistry


@cli_command(name="print-user-id")
async def print_user_id(registry: MyRegistry, username: str):
    user = await registry.uow.users.get_user_by_username(username)
    print(user.user_id if user else "")
