from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from core.models.models import *
from settings import config_parameters

tortoise_credentials = {
    "host": config_parameters.POSTGRES_DB_HOST,
    "port": config_parameters.POSTGRES_DB_PORT,
    "user": config_parameters.POSTGRES_DB_USERNAME,
    "password": config_parameters.POSTGRES_DB_PASSWORD,
    "database": config_parameters.POSTGRES_DB_NAME,
}

tortoise_connection_config = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": tortoise_credentials,
            "max_size": 1000,
        }
    },
    "apps": {
        "models": {
            "models": ["core.models.models"],
            "default_connection": "default",
        }
    },
}


async def init_db():
    await Tortoise.init(config=tortoise_connection_config)
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()


def init(server: FastAPI):
    register_tortoise(server, config=tortoise_connection_config, generate_schemas=True)
