import logging
import os
import pathlib
import backoff
from contextlib import contextmanager
from typing import Any

import psycopg2
from psycopg2.extras import DictCursor, register_uuid

from config.base import CONFIG, BACKOFF_CONFIG
from config.logger import logger


@contextmanager
@backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
def pg_conn_context():
    conn = psycopg2.connect(**CONFIG.dsl(), cursor_factory=DictCursor)

    yield conn

    conn.close()


if __name__ == "__main__":
    logger.info("*** Start initialize postgres ***")
    schema_file = os.path.join(pathlib.Path(__file__).parent.absolute(), "schema.sql")

    with pg_conn_context() as pg_conn, pg_conn.cursor() as pg_cursor:
        logger.info("[+] PG connecting successfully...")

        with open(schema_file, "r") as schema_fd:
            pg_cursor.execute(schema_fd.read())

        register_uuid()

        pg_conn.commit()
        logger.info("[+] PG initialize successfully...")
