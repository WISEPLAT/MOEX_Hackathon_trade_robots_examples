from redis import Redis
from loguru import logger

from src.extract.tradestat import TradestatExtractor
from src.core.config import POSTGRES_CONFIG, REDIS_CONFIG, NODES
from src.load.clickhouse import ClickhouseLoader
from src.transform.tradestat import TradestatTransformer
from src.transform.ticker import TickerBriefTransformer
from src.state.redis import RedisState
from src.extract.postgres import PostgreSQLExtractor


def run():
    batch_size = 100000
    tickers_extractor = PostgreSQLExtractor(settings=POSTGRES_CONFIG)
    tickers_transformer = TickerBriefTransformer()

    raw_tickers = tickers_extractor.extract()
    tickers = tickers_transformer.transform(raw_tickers)

    redis = Redis(
        host=REDIS_CONFIG.HOST, port=REDIS_CONFIG.PORT, password=REDIS_CONFIG.PASSWORD
    )
    state = RedisState(redis=redis)

    extractor = TradestatExtractor(state=state)
    tradestat_transformer = TradestatTransformer()

    for ticker in tickers:
        logger.info(f'Starting {ticker.secid}')

        while state.get(f'status::tradestat::{ticker.secid}', 0) == 0 and state.get(f'extracting::tradestat::{ticker.secid}', 0) == 0:
            raw_data = extractor.extract(ticker=ticker, block_size=batch_size)

            data = tradestat_transformer.transform(data=raw_data, ticker=ticker.secid)

            loader = ClickhouseLoader(
                host=NODES[2].HOST,
                port=NODES[2].PORT,
                user=NODES[2].USER,
                password=NODES[2].PASSWORD,
                alt_hosts=[f"{NODE.HOST}:{NODE.PORT}" for NODE in NODES],
                state=state,
                batch_size=batch_size,
            )

            loader.load(data=data, table="tradestats", key=f'tradestat::{ticker.secid}')
