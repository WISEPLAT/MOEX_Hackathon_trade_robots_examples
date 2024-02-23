from typing import Optional

import backoff
from config.base import BACKOFF_CONFIG
from config.logger import logger
from clickhouse_driver import Client as Clickhouse


def ch_conn_is_alive(ch_conn: Clickhouse) -> bool:
    """Функция для проверки работоспособности Clickhouse"""
    try:
        return ch_conn.execute("SHOW DATABASES")
    except Exception:
        return False


class ClickhouseClient:
    def __init__(
        self,
        host: str,
        port: int,
        user: str = "default",
        password: str = "",
        conn: Optional[Clickhouse] = None,
    ) -> None:
        self._conn: Clickhouse = conn
        self._host: str = host
        self._port: int = port
        self._user: str = user
        self._password: str = password

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
            host=self._host, port=self._port, user=self._user, password=self._password
        )

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def create(self, ddl_file: str | None = None, content: str | None = None):
        logger.info('[*] Initialized clickhouse node: "%s:%d"', self._host, self._port)
        logger.info('[*] Reading schema from file: "%s"', ddl_file)

        if ddl_file is None and content is None:
            raise ValueError('ddl_file and content is "None"')

        if ddl_file is not None:
            with open(ddl_file, "r") as fd:
                schema = fd.read()
        else:
            schema = content

        for command in schema.split(";"):
            command = command.strip()

            if len(command) == 0:
                continue

            logger.info('[*] Command: "%s"', command)
            self.conn.execute(command)
