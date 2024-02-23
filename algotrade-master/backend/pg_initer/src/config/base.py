from typing import Any

import backoff
from pydantic import Field
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    USER: str = Field()
    PASSWORD: str = Field()
    HOST: str = Field()
    PORT: int = Field()
    NAME: str = Field()

    class Config:
        env_prefix = "DB_"

    def dsl(self) -> dict[str, Any]:
        return {
            "dbname": self.NAME,
            "user": self.USER,
            "password": self.PASSWORD,
            "host": self.HOST,
            "port": self.PORT,
        }


CONFIG: PostgresSettings = PostgresSettings()
BACKOFF_CONFIG: dict[str, Any] = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "max_value": 8,
}
