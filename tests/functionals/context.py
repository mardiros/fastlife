from playwright.sync_api import Page, Response


class Context:
    browser: Page
    text: str
    response: Response | None
