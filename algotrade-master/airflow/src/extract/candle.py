import backoff
from moexalgo import Ticker
from typing import Iterator, Any
from dataclasses import dataclass
from loguru import logger
from datetime import datetime, date

from src.extract.base import BaseExtractor
from src.models.ticker import TickerBriefModel
from src.state.base import BaseState
from src.core.config import BACKOFF_CONFIG


@dataclass
class CandleExtractor(BaseExtractor):
    state: BaseState

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def extract(
        self,
        ticker: TickerBriefModel,
        period: int = 1,
        batch_size: int = 10000,
        block_size: int = 100000
    ) -> Iterator[dict[str, Any]]:

        ticker_ts = Ticker(secid=ticker.secid)

        key = f'candle::{ticker.secid}'
        extracting_key = f'extracting::{key}'
        
        if self.state.get(extracting_key, 0):
            logger.info(f'Already running {extracting_key}')
            return

        self.state.set(extracting_key, 1, expire=None)

        _block_size = 0
        while _block_size < block_size:
            down_limit = datetime.fromisoformat(self.state.get(
                key, default_value=date(year=1970, month=1, day=1).isoformat()
            ))
            logger.info(f'Redis cache: {down_limit}')

            candles = ticker_ts.candles(
                date=down_limit.date().isoformat(),
                till_date=date.today().isoformat(),
                period=period,
                limit=batch_size
            )

            i = 0

            for candle in candles:
                i += 1
                if candle.begin < down_limit:
                    logger.info(f'Already extract. Begin: {candle.begin} | {key}::{down_limit}')
                    continue

                yield candle

            _block_size += i
            if i < batch_size or _block_size % block_size == 0:
                self.state.set(f'status::{key}', i < batch_size)

                logger.info(f'Extracted: {i} | block_size: {_block_size}')
                
                self.state.set(extracting_key, 0)
                return
