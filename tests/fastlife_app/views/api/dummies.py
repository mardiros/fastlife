from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from fastlife.config.views import view_config


class Dummy(BaseModel):
    name: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://token")


@view_config(
    "list_dummies",
    "/api/dummies",
    permission="dummies:read",
    methods=["GET"],
    summary="API For Dummies",
    description="Fetch a list of dummies.",
    response_description="Dummies collection",
    tags=["dummies"],
)
async def list_dummies(
    response: Response, token: str = Depends(oauth2_scheme)
) -> list[Dummy]:
    response.headers["Total-Count"] = "2"
    return [Dummy(name="Foo"), Dummy(name="Bar")]
