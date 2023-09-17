import secrets


def create_csrf_token() -> str:
    return secrets.token_urlsafe(5)
