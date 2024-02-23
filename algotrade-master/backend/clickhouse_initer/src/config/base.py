from typing import Any

import backoff
from pydantic import Field
from pydantic_settings import BaseSettings


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


CLICKHOUSE_CONFIG: ClickhouseSettings = ClickhouseSettings()
BACKOFF_CONFIG: dict[str, Any] = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "max_value": 8,
}
