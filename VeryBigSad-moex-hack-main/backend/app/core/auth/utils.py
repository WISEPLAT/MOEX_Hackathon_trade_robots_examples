from typing import Any

from settings import config_parameters


def get_refresh_token_settings(
    refresh_token: str,
    expired: bool = False,
) -> dict[str, Any]:
    base_cookie = {
        "key": config_parameters.REFRESH_TOKEN_KEY,
        "httponly": True,
        "samesite": "none",
        "secure": config_parameters.SECURE_COOKIES,
        "domain": config_parameters.SITE_DOMAIN,
    }
    if expired:
        return base_cookie

    return {
        **base_cookie,
        "value": refresh_token,
        "max_age": config_parameters.REFRESH_TOKEN_EXP,
    }
