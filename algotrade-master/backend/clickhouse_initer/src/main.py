from jinja2 import Environment, FileSystemLoader

from config.nodes import NODES
from config.base import CLICKHOUSE_CONFIG
from config.logger import logger
from clickhouse.client import ClickhouseClient
from clickhouse.loader import ClickhouseLoader
from extractor.file import CSVExtractor
from transformer.movie_frame import MovieFrameTransformer


if __name__ == "__main__":
    environment = Environment(loader=FileSystemLoader("./mapping/"))

    for NODE in NODES:
        logger.info("[*] Start creating mapping")

        ch_initer = ClickhouseClient(
            host=NODE.HOST, port=NODE.PORT, user=NODE.USER, password=NODE.PASSWORD
        )

        template = environment.get_template("node.sql.j2")
        schema = template.render(
            node=NODE,
        )

        ch_initer.create(content=schema)

    if CLICKHOUSE_CONFIG.INIT_DATA and CLICKHOUSE_CONFIG.INIT_DATA_PATH is not None:
        logger.info("[*] Start init data")
        logger.info("[*] Connecting into clickhouse")

        client = ClickhouseClient(
            host=NODES[0].HOST,
            port=NODES[0].PORT,
            user=NODES[0].USER,
            password=NODES[0].PASSWORD,
        )

        extractor = CSVExtractor(
            file_path=CLICKHOUSE_CONFIG.INIT_DATA_PATH,
            headers=["user_id", "movie_id", "rating"],
        )
        transformer = MovieFrameTransformer()
        loader = ClickhouseLoader(client=client)

        logger.info("[*] Extract data")
        raw_data = extractor.extract()
        logger.info("[+] Successfull extract data")

        logger.info("[*] Transform data")
        transformed_data = transformer.transform(raw_data)
        logger.info("[+] Successfull transform data")

        logger.info("[*] Load data")
        loader.insert(table=CLICKHOUSE_CONFIG.INIT_TABLE, data=transformed_data)
        logger.info("[+] Successfull load data")
