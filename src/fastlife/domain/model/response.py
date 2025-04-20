from collections.abc import Mapping
from urllib.parse import quote

from starlette.background import BackgroundTask
from starlette.datastructures import URL
from starlette.responses import Response


class RedirectResponse(Response):
    """
    A redirect response for Post/Redirect/Get pattern.

    The starlette default value status code is 307, which means that it is used
    as a way to replay the same query which is definitly not the most used case
    in web applications.

    This is why the redirect response here is using 303 see other which
    ensure a GET request will be made for the redirection.

    A new parameter hx_redirect exists in order to set the HX-Redirect header
    to follow a browser redirection from an ajax query.
    """

    def __init__(
        self,
        url: str | URL,
        hx_redirect: bool = False,
        status_code: int = 303,
        headers: Mapping[str, str] | None = None,
        background: BackgroundTask | None = None,
    ):
        super().__init__(
            content=b"", status_code=status_code, headers=headers, background=background
        )
        self.headers["HX-Redirect" if hx_redirect else "location"] = quote(
            str(url), safe=":/%#?=@[]!$&'()*+,;"
        )


__all__ = ["Response", "RedirectResponse"]
