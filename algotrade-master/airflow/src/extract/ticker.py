from moexalgo.market import Market
from typing import Iterator, Any
from dataclasses import dataclass

from src.extract.base import BaseExtractor


@dataclass
class TickerExtractor(BaseExtractor):
    market = Market(name='shares', boardid='TQBR')

    def extract(self) -> Iterator[dict[str, Any]]:
        yield from self.market.tickers()
