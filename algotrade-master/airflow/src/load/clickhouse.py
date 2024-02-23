from typing import Optional, Iterator, Any

import backoff
from loguru import logger
from clickhouse_driver import Client as Clickhouse
from datetime import datetime, date

from src.core.config import BACKOFF_CONFIG
from src.load.base import BaseLoader
from src.state.base import BaseState


def ch_conn_is_alive(ch_conn: Clickhouse) -> bool:
    """Функция для проверки работоспособности Clickhouse"""
    try:
        return ch_conn.execute("SHOW DATABASES")
    except Exception:
        return False


class ClickhouseLoader(BaseLoader):
    def __init__(
        self,
        state: BaseState,
        host: str,
        port: int,
        user: str = "default",
        password: str = "",
        alt_hosts: list[str] | None = None,
        conn: Clickhouse | None = None,
        settings: dict[str, Any] | None = None,
        batch_size: int = 100000,
    ) -> None:
        self._conn: Clickhouse = conn
        self._host: str = host
        self._alt_hosts: list[str] | None = alt_hosts
        self._port: int = port
        self._user: str = user
        self._password: str = password
        self._settings: dict[str, Any] | None = settings
        self._state = state
        self._batch_size = batch_size

    @property
    def conn(self) -> Clickhouse:
        if self._conn is None or not ch_conn_is_alive(self._conn):
            self._conn = self._reconnection()

        return self._conn

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def _reconnection(self) -> Clickhouse:
        logger.info('Reconnection clickhouse node "%s:%d" ...', self._host, self._port)

        if self._conn is not None:
            logger.info("Closing already exists clickhouse connector...")
            self._conn.disconnect()

        return Clickhouse(
            host=self._host,
            port=self._port,
            user=self._user,
            alt_hosts=",".join(self._alt_hosts),
            password=self._password,
            settings=self._settings,
        )
    
    def _load(self, data: Iterator[dict[str, Any]], key: str) -> Iterator[type]:
        i = 0
        
        down_limit = datetime.fromisoformat(
            self._state.get(key, date(year=1970, month=1, day=1).isoformat())
        )
        
        for elem in data:
            i += 1
            
            down_limit = max(elem.get('end') or elem.get('ts'), down_limit)

            yield elem

            self._state.set(key, down_limit.isoformat(), expire=None)

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def load(self, data: Iterator[dict[str, Any]], table: str, key: str | None = None) -> int | None:

        data_gen = data if key is None else self._load(data=data, key=key)

        lines = self.conn.execute(
            f"INSERT INTO {table} VALUES ", data_gen
        )

        logger.info(f'Inserted "{lines}" lines into clickhouse')
        
        return lines
