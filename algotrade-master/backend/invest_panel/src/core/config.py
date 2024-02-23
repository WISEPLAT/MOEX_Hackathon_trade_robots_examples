import backoff
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Any


class AppSettings(BaseSettings):
    HOST: str = Field("localhost")
    PORT: int
    PROJECT_NAME: str
    API_PATH: str
    API_URL: str
    SCHEMA_REGISTRY_URL: str = Field("http://localhost:8081")
    API_VERSION: str
    SWAGGER_PATH: str
    JSON_SWAGGER_PATH: str
    PAGE_SIZE: int

    class Config:
        env_prefix = "INVEST_PANEL_"


class PostgresSettings(BaseSettings):
    SCHEMA: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

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
    
    @property
    def URL(self):
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}'
    

class RedisSettings(BaseSettings):
    PASSWORD: str
    HOST: str
    PORT: int
    CACHE_EXPIRE: int

    class Config:
        env_prefix = "REDIS_"


class ClickhouseSettings(BaseSettings):
    NODES: str
    INIT_TABLE: str
    INIT_DATA: bool = Field(False)
    INIT_DATA_PATH: str | None

    @classmethod
    def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
        if field_name.upper() == "NODES":
            return [x for x in raw_val.split(",")]
        return cls.json_loads(raw_val)

    class Config:
        env_prefix = "CH_"


class AlgotradeSettingsNode01(BaseSettings):
    DISTRIBUTED_TABLE: str
    REPLICA_PATH: str
    REPLICA_NAME: str

    class Config:
        env_prefix = "CLICKHOUSE_NODE01_ALGOTRADE_"


class ClickhouseNode01(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    CLUSTER: str
    STATUS_ROUTE: BaseSettings = Field(default_factory=AlgotradeSettingsNode01)

    class Config:
        env_prefix = "CLICKHOUSE_NODE01_"


class AlgotradeSettingsNode02(BaseSettings):
    DISTRIBUTED_TABLE: str
    REPLICA_PATH: str
    REPLICA_NAME: str

    class Config:
        env_prefix = "CLICKHOUSE_NODE02_ALGOTRADE_"


class ClickhouseNode02(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    CLUSTER: str
    STATUS_ROUTE: BaseSettings = Field(default_factory=AlgotradeSettingsNode02)

    class Config:
        env_prefix = "CLICKHOUSE_NODE02_"


class AlgotradeSettingsNode03(BaseSettings):
    DISTRIBUTED_TABLE: str
    REPLICA_PATH: str
    REPLICA_NAME: str

    class Config:
        env_prefix = "CLICKHOUSE_NODE03_ALGOTRADE_"


class ClickhouseNode03(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    CLUSTER: str
    STATUS_ROUTE: BaseSettings = Field(default_factory=AlgotradeSettingsNode03)

    class Config:
        env_prefix = "CLICKHOUSE_NODE03_"


class AlgotradeSettingsNode04(BaseSettings):
    DISTRIBUTED_TABLE: str
    REPLICA_PATH: str
    REPLICA_NAME: str

    class Config:
        env_prefix = "CLICKHOUSE_NODE04_ALGOTRADE_"


class ClickhouseNode04(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    CLUSTER: str
    STATUS_ROUTE: BaseSettings = Field(default_factory=AlgotradeSettingsNode04)

    class Config:
        env_prefix = "CLICKHOUSE_NODE04_"


class AlgotradeSettingsNode05(BaseSettings):
    DISTRIBUTED_TABLE: str
    REPLICA_PATH: str
    REPLICA_NAME: str

    class Config:
        env_prefix = "CLICKHOUSE_NODE05_ALGOTRADE_"


class ClickhouseNode05(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    CLUSTER: str
    STATUS_ROUTE: BaseSettings = Field(default_factory=AlgotradeSettingsNode05)

    class Config:
        env_prefix = "CLICKHOUSE_NODE05_"


class AlgotradeSettingsNode06(BaseSettings):
    DISTRIBUTED_TABLE: str
    REPLICA_PATH: str
    REPLICA_NAME: str

    class Config:
        env_prefix = "CLICKHOUSE_NODE06_ALGOTRADE_"


class ClickhouseNode06(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    CLUSTER: str
    STATUS_ROUTE: BaseSettings = Field(default_factory=AlgotradeSettingsNode06)

    class Config:
        env_prefix = "CLICKHOUSE_NODE06_"


NODES = [
    ClickhouseNode01(),
    ClickhouseNode02(),
    ClickhouseNode03(),
    ClickhouseNode04(),
    ClickhouseNode05(),
    ClickhouseNode06(),
]

CLICKHOUSE_CONFIG: ClickhouseSettings = ClickhouseSettings()


POSTGRES: PostgresSettings = PostgresSettings()


class Config(BaseSettings):
    APP: AppSettings = AppSettings()


CONFIG = Config()
REDIS_CONFIG = RedisSettings()
BACKOFF_CONFIG: dict[str, Any] = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "max_value": 8,
}
