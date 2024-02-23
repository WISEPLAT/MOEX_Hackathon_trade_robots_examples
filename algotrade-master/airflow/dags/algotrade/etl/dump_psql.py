import gzip
from datetime import datetime

from loguru import logger
from sh import pg_dump

from src.core.config import POSTGRES_CONFIG


def run():
    with gzip.open(
        f'/tmp/backups/dump-{POSTGRES_CONFIG.NAME}-{datetime.now().strftime("%Y-%m-%d")}.sql.gz',
        "wb",
    ) as fd:
        content = pg_dump(
            "--dbname",
            (
                f"postgresql://{POSTGRES_CONFIG.USER}:{POSTGRES_CONFIG.PASSWORD}"
                f"@{POSTGRES_CONFIG.HOST}:{POSTGRES_CONFIG.PORT}/{POSTGRES_CONFIG.NAME}"
            ),
        )
        fd.write(content.encode())

    logger.info(f'[+] Success finished dump "{POSTGRES_CONFIG.NAME}" database')