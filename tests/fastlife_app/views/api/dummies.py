from fastapi import Depends, Response
from pydantic import BaseModel

from fastlife import Configurator, configure
from fastapi.security import OAuth2PasswordBearer


class Dummy(BaseModel):
    name: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://token")


async def list_dummies(
    response: Response, token: str = Depends(oauth2_scheme)
) -> list[Dummy]:
    response.headers["Total-Count"] = "2"
    return [Dummy(name="Foo"), Dummy(name="Bar")]


@configure
def includeme(config: Configurator):
    config.add_api_route(
        "list_dummies",
        "/api/dummies",
        list_dummies,
        permission="dummies:read",
        methods=["GET"],
        summary="API For Dummies",
        description="Fetch a list of dummies.",
        response_description="Dummies collection",
        tags=["dummies"],
    )
