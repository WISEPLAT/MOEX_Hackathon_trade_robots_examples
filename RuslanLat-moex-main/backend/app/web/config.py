import typing
import yaml
from dataclasses import dataclass


if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass
class YandexConfig:
    key: str


@dataclass
class Config:
    #admin: AdminConfig
    session: SessionConfig = None
    database: DatabaseConfig = None
    yandex_api: YandexConfig = None


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        session=SessionConfig(
            key=raw_config["session"]["key"],
        ),
        database=DatabaseConfig(**raw_config["database"]),
    )
