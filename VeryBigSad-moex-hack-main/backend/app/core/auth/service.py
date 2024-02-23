import uuid
from datetime import datetime, timedelta
from typing import Any

from pydantic import UUID4

from core.auth.exceptions import InvalidCredentials
from core.auth.security import check_password
from core.schemas.auth import AuthUser


async def create_user(user: AuthUser) -> dict[str, Any] | None:
    # TODO
    pass


async def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    # TODO
    pass


async def get_user_by_email(email: str) -> dict[str, Any] | None:
    # TODO
    pass


async def create_refresh_token(
    *, user_id: int, refresh_token: str | None = None
) -> str:
    # if not refresh_token:
    #     refresh_token = utils.generate_random_alphanum(64)
    #
    # insert_query = refresh_tokens.insert().values(
    #     uuid=uuid.uuid4(),
    #     refresh_token=refresh_token,
    #     expires_at=datetime.utcnow() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
    #     user_id=user_id,
    # )
    # await execute(insert_query)
    #
    # return refresh_token
    pass


async def get_refresh_token(refresh_token: str) -> dict[str, Any] | None:
    pass


async def expire_refresh_token(refresh_token_uuid: UUID4) -> None:
    pass


async def authenticate_user(auth_data: AuthUser) -> dict[str, Any]:
    user = await get_user_by_email(auth_data.email)
    if not user:
        raise InvalidCredentials()

    if not check_password(auth_data.password, user["password"]):
        raise InvalidCredentials()

    return user
