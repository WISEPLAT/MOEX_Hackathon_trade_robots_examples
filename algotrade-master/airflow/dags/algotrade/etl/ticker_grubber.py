from src.extract.ticker import TickerExtractor
from src.core.config import POSTGRES_CONFIG
from src.load.postgres import PostgresLoader
from src.transform.ticker import TickerTransformer, TickerModel
from src.schema import SCHEMA, Schema


def run():
    extractor = TickerExtractor()

    ticker_transformer = TickerTransformer()

    raw_data = extractor.extract()

    data = ticker_transformer.transform(data=raw_data)

    loader = PostgresLoader(
        settings=POSTGRES_CONFIG,
        metadata={
            Schema.TICKERS: TickerModel,
        },
        schema=SCHEMA,
    )
    with loader:
        loader.load(
            {Schema.TICKERS: data,},
            truncate_before=True,
        )
