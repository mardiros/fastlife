from playwright.async_api import Page
from tursu import given, when


@given('anonymous user on "{path}"')
@when('I visit "{path}"')
async def i_visit(page: Page, path: str, fastlife_app: str):
    # page.on("request", lambda req: print(f"***** request: {req.url}"))
    # page.on("response", lambda res: print(f"***** response: {res.status} {res.url}"))
    await page.goto(f"{fastlife_app}{path}")
