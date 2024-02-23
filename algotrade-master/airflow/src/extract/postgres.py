from typing import Any, Iterator
from loguru import logger

import backoff
import psycopg2
from core.config import BACKOFF_CONFIG, PostgresSettings
from src.schema import Schema
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor


class PostgreSQLExtractor:
    """Класс для извлечения сырых данных из постгрес"""

    def __init__(
        self, settings: PostgresSettings,
        pg_conn: connection | None = None,
        chunk_size: int = 1000
    ):
        self._pg_conn = pg_conn
        self._settings = settings
        self.chunk_size = chunk_size

    # @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def _reconnection(self) -> connection:
        """Метод подключения/переподключения к бд"""

        if self._pg_conn is not None:
            self._pg_conn.close()

        return psycopg2.connect(**self._settings.dsn(), cursor_factory=DictCursor)

    @property
    def pg_conn(self) -> connection:
        if self._pg_conn is None or self._pg_conn.closed:
            self._pg_conn = self._reconnection()

        return self._pg_conn

    # @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def extract(self) -> Iterator[tuple[Any]]:
        """Метод получения сырых данных из бд.
        В результате возвращаю генератор, которых позволяет брать
        данные из бд сразу пачкой по chunk_size штук"""

        cursor = self.pg_conn.cursor()
        cursor.itersize = self.chunk_size

        query = (
            f'SELECT t.secid FROM {self._settings.SCHEMA}.{Schema.TICKERS} t '
        )
        cursor.execute(query)

        for row in cursor:
            yield row

        cursor.close()
