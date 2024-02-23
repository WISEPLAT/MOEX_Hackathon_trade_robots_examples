from typing import Any, Iterator

from src.transform.base import BaseTransformer
from src.models.tradestat import TradestatModel


class TradestatTransformer(BaseTransformer):
    def transform(self, data: Iterator[Any], ticker: str, to_dict: bool = False) -> Iterator[Any]:

        for elem in data:
            elem = TradestatModel(
                secid=ticker,
                ts=elem.ts,
                pr_open=elem.pr_open,
                pr_close=elem.pr_close,
                pr_change=elem.pr_change,
                pr_high=elem.pr_high,
                pr_low=elem.pr_low,
                pr_std=elem.pr_std,
                pr_vwap=elem.pr_vwap,
                pr_vwap_b=elem.pr_vwap_b,
                pr_vwap_s=elem.pr_vwap_s,
                val=elem.val,
                val_b=elem.val_b,
                val_s=elem.val_s,
                vol=elem.vol,
                vol_b=elem.vol_b,
                vol_s=elem.vol_s,
                trades=elem.trades,
                trades_b=elem.trades_b,
                trades_s=elem.trades_s,
                disb=elem.disb
            )
            yield elem.model_dump()
