from abc import ABC, abstractmethod
from typing import Iterator, Any

import backoff
from loguru import logger
from clickhouse_driver import Client as Clickhouse

from src.core.config import BACKOFF_CONFIG


def ch_conn_is_alive(ch_conn: Clickhouse) -> bool:
    """Функция для проверки работоспособности Clickhouse"""
    try:
        return ch_conn.execute('SHOW DATABASES')
    except Exception:
        return False


class BaseRepository(ABC):
    @property
    @abstractmethod
    def table(self) -> str:
        """Имя дистрибутивной таблицы"""

    def __init__(
        self,
        host: str,
        port: int,
        user:str = 'default',
        password: str = '',
        alt_hosts: list[str] | None = None,
        conn: Clickhouse | None = None,
        settings: dict[str, Any] | None = None
    ) -> None:
        self._conn: Clickhouse = conn
        self._host: str = host
        self._alt_hosts: list[str] | None = alt_hosts
        self._port: int = port
        self._user: str = user
        self._password: str = password
        self._settings: dict[str, Any] | None = settings

    @property
    def conn(self) -> Clickhouse:
        if self._conn is None or not ch_conn_is_alive(self._conn):
            self._conn = self._reconnection()

        return self._conn

    # @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def _reconnection(self) -> Clickhouse:
        logger.info('Reconnection clickhouse node "%s:%d" ...', self._host, self._port)

        if self._conn is not None:
            logger.info('Closing already exists clickhouse connector...')
            self._conn.disconnect()

        return Clickhouse(
            host=self._host,
            port=self._port,
            user=self._user,
            alt_hosts=','.join(self._alt_hosts),
            password=self._password,
            settings=self._settings,
        )

    # @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def time_series(
        self,
        *,
        fields: list[str],
        where: list[str] | None = None,
        group_by: list[str] | None = None,
        order_by: dict[str, str] | None = None,
        limit: int = 100000,
        **kwargs
    ) -> Iterator[Any]:
        offset = 0

        query = (
            f'SELECT {", ".join(fields)} FROM {self.table} '
        )

        if where is not None and len(where) > 0:
            query += f'WHERE {" AND ".join(where)} '

        if group_by is not None:
            query += f'GROUP BY {", ".join(group_by)} '

        if order_by is not None:
            query += 'ORDER BY '
            if 'asc' in order_by.keys() and isinstance(order_by['asc'], list):
                query += f'{" ASC, ".join(order_by["asc"])} ASC '
            if 'desc' in order_by.keys() and isinstance(order_by['desc'], list):
                query += f'{" DESC, ".join(order_by["desc"])} DESC '

        while (
            result_df := self.conn.query_dataframe(    
                f'{query} LIMIT {offset}, {limit}'
            )
        ) is not None and not result_df.empty:
            offset += limit

            for _, series in result_df.iterrows():
                yield series.to_dict()
