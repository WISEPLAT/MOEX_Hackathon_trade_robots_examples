from typing import Any, Iterator
from loguru import logger
from psycopg2 import connect as pg_connect
from psycopg2.extras import DictCursor, execute_values

from src.load.base import BaseLoader
from src.core.config import PostgresSettings


class PostgresLoader(BaseLoader):
    def __init__(
        self,
        settings: PostgresSettings,
        metadata: dict[str, Any],
        schema: str = "public",
        chunk_size: int = 1000,
    ):
        self._settings = settings
        self._metadata = metadata
        self._schema = schema
        self._cursor = None
        self._loaded_data = {schema_name: [] for schema_name in self._metadata.keys()}
        self._chunk_size = chunk_size

    def __enter__(self):
        conn = pg_connect(**self._settings.dsn(), cursor_factory=DictCursor)
        self._cursor = conn.cursor()
        return self

    def __exit__(self, *args, **kwargs):
        self._cursor.close()

    def _multiple_insert(self, insert_query: str, data: list[tuple[Any]]) -> None:
        execute_values(self._cursor, insert_query, data)

    def _get_values_statement(
        self, into_statement: list[str], data: type
    ) -> tuple[Any]:
        try:
            data_as_dict: dict[str, Any] = data.model_dump()
        except:
            logger.error("Oops")
        return tuple(data_as_dict[key] for key in into_statement)

    def _save_data(self, schema_name: str) -> None:
        schema: type = self._metadata.get(schema_name)
        data: Iterator[type] = self._loaded_data[schema_name]

        if not isinstance(schema, type):
            message = f"Error with saving dataclass: {schema_name}. Message: is not dataclass type."
            logger.error(message)
            raise TypeError(message)

        into_statement: list[str] = [field for field in schema.__fields__.keys()]
        insert_query: str = (
            f"INSERT INTO {self._schema}.{schema_name}"
            f'({", ".join(into_statement)}) '
            f"VALUES %s ON CONFLICT (id) DO NOTHING "
        )

        self._multiple_insert(
            insert_query,
            (
                self._get_values_statement(into_statement=into_statement, data=elem)
                for elem in data
            ),
        )

        logger.debug(f"Success multiple insert {schema_name} ({len(data)} objects)")

    def _stack_or_flush(self, schema_name: str, data: type | None, is_last: bool):
        if data is not None:
            self._loaded_data[schema_name].append(data)

        if len(self._loaded_data[schema_name]) == self._chunk_size or is_last:
            self._save_data(schema_name=schema_name)
            self._loaded_data.update({schema_name: []})
            logger.debug(f"Chunk from {schema_name} schema has been flushed!")

    def _stack_or_flush_all_data(
        self, obj: dict[str, type], schema_name: str, is_last: bool = False
    ) -> None:
        try:
            self._stack_or_flush(schema_name=schema_name, data=obj, is_last=is_last)

            self._cursor.execute("COMMIT;")

        except Exception as err:
            self._cursor.execute("ROLLBACK;")

            logger.error(f"Error stack or flush data! Message: {err}")
            raise err

    def _truncate(self, schema_name: str) -> None:
        self._cursor.execute(f"TRUNCATE TABLE {self._schema}.{schema_name};")

    def load(self, data: Iterator[dict[str, Any]], truncate_before: bool = False):
        logger.info("Start saving all data to PostgreSQL database instance.")

        for schema_name in self._metadata.keys():
            if truncate_before:
                self._truncate(schema_name=schema_name)

            for obj in data[schema_name]:
                self._stack_or_flush_all_data(obj, schema_name)

        for schema_name in self._metadata.keys():
            self._stack_or_flush_all_data(
                obj=None, schema_name=schema_name, is_last=True
            )

        logger.info("Success finish saving all data to PostgreSQL database instance.")

    def execute(self, query: str):
        return self._cursor.execute(query)
