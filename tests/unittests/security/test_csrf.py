import pytest

from fastlife.adapters.fastapi.request import Request
from fastlife.domain.model.csrf import create_csrf_token
from fastlife.service.csrf import CSRFAttack, check_csrf


def test_create_csrf_token():
    token = create_csrf_token()
    assert len(token) == 7
    assert token != create_csrf_token()


@pytest.mark.parametrize(
    "params",
    [
        pytest.param({"request": {"method": "GET"}}, id="GET query does not validate"),
        pytest.param(
            {
                "request": {
                    "method": "POST",
                    "headers": {"content-type": "application/json"},
                }
            },
            id="POST for application/json is ignored",
        ),
        pytest.param(
            {
                "request": {
                    "method": "POST",
                    "headers": {
                        "content-type": "application/x-www-form-urlencoded",
                        "cookie": "csrf_token=xxx",
                    },
                    "body": "foo=bar&csrf_token=xxx",
                }
            },
            id="POST query are validated only for application/x-www-form-urlencoded",
        ),
    ],
)
async def test_check_csrf(dummy_request_param: Request):
    assert await check_csrf()(dummy_request_param) is True


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "request": {
                    "method": "POST",
                    "headers": {
                        "content-type": "application/x-www-form-urlencoded",
                    },
                    "body": "foo=bar&csrf_token=xxx",
                }
            },
            id="no cookie",
        ),
        pytest.param(
            {
                "request": {
                    "method": "POST",
                    "headers": {
                        "content-type": "application/x-www-form-urlencoded",
                        "cookie": "csrf_token=xxx",
                    },
                    "body": "foo=bar",
                }
            },
            id="no body value",
        ),
        pytest.param(
            {
                "request": {
                    "method": "POST",
                    "headers": {
                        "content-type": "application/x-www-form-urlencoded",
                        "cookie": "csrf_token=xxx",
                    },
                    "body": "foo=bar&csrf_token=yyy",
                }
            },
            id="not match",
        ),
    ],
)
async def test_check_csrf_raises(dummy_request_param: Request):
    with pytest.raises(CSRFAttack):
        await check_csrf()(dummy_request_param)
