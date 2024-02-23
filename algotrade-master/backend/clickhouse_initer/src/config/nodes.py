from pydantic import Field
from pydantic_settings import BaseSettings


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
    ALGOTRADE: BaseSettings = Field(default_factory=AlgotradeSettingsNode01)

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
    ALGOTRADE: BaseSettings = Field(default_factory=AlgotradeSettingsNode02)

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
    ALGOTRADE: BaseSettings = Field(default_factory=AlgotradeSettingsNode03)

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
    ALGOTRADE: BaseSettings = Field(default_factory=AlgotradeSettingsNode04)

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
    ALGOTRADE: BaseSettings = Field(default_factory=AlgotradeSettingsNode05)

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
    ALGOTRADE: BaseSettings = Field(default_factory=AlgotradeSettingsNode06)

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
