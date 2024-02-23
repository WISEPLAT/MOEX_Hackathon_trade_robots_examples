from typing import Union

from pydantic import BaseModel


class MetaConfigsModel(BaseModel):
    IS_PROD: Union[bool] = True


class APIConfigsModel(BaseModel):
    API_HOST: Union[str]
    API_PORT: Union[int]
    SITE_DOMAIN: Union[str]


class PostgresDataBaseConfigsModel(BaseModel):
    POSTGRES_DB_USERNAME: Union[str]
    POSTGRES_DB_PASSWORD: Union[str]
    POSTGRES_DB_HOST: Union[str]
    POSTGRES_DB_PORT: Union[int]
    POSTGRES_DB_NAME: Union[str]


class AuthConfigsModel(BaseModel):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 5  # minutes

    REFRESH_TOKEN_KEY: str = "refreshToken"
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 28  # 28 days

    SECURE_COOKIES: bool = True


class ConfigsValidator(
    APIConfigsModel,
    PostgresDataBaseConfigsModel,
    MetaConfigsModel,
    AuthConfigsModel
):
    pass
