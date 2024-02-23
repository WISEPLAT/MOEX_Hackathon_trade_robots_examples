from clickhouse.client import ClickhouseClient
from dataclasses import dataclass
from typing import Iterator

from models.movie import MovieFrameDatagram


@dataclass
class ClickhouseLoader:
    client: ClickhouseClient

    def insert(self, table: str, data: Iterator[MovieFrameDatagram]) -> None:
        self.client.conn.execute(
            f"INSERT INTO {table} VALUES", (_.dict() for _ in data)
        )
