from typing import Any, Iterator

from src.transform.base import BaseTransformer
from src.models.obstat import OBstatModel


class OBstatTransformer(BaseTransformer):
    def transform(self, data: Iterator[Any], ticker: str, to_dict: bool = False) -> Iterator[Any]:

        for elem in data:
            elem = OBstatModel(
                secid=ticker,
                ts=elem.ts,
                spread_1mio=elem.spread_1mio,
                spread_bbo=elem.spread_bbo,
                spread_lv10=elem.spread_lv10,
                levels_b=elem.levels_b,
                levels_s=elem.levels_s,
                vol_b=elem.vol_b,
                vol_s=elem.vol_s,
                val_b=elem.val_b,
                val_s=elem.val_s,
                imbalance_val=elem.imbalance_val,
                imbalance_val_bbo=elem.imbalance_val_bbo,
                imbalance_vol=elem.imbalance_vol,
                imbalance_vol_bbo=elem.imbalance_vol_bbo,
                vwap_b=elem.vwap_b,
                vwap_b_1mio=elem.vwap_b_1mio,
                vwap_s=elem.vwap_s,
                vwap_s_1mio=elem.vwap_s_1mio,
            )
            yield elem.model_dump()
