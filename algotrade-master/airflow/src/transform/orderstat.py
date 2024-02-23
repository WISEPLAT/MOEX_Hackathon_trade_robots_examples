from typing import Any, Iterator

from src.transform.base import BaseTransformer
from src.models.orderstat import OrderstatModel


class OrderstatTransformer(BaseTransformer):
    def transform(self, data: Iterator[Any], ticker: str, to_dict: bool = False) -> Iterator[Any]:

        for elem in data:
            elem = OrderstatModel(
                secid=ticker,
                ts=elem.ts,
                put_orders=elem.put_orders,
                put_orders_b=elem.put_orders_b,
                put_orders_s=elem.put_orders_s,
                cancel_orders=elem.cancel_orders,
                cancel_orders_b=elem.cancel_orders_b,
                cancel_orders_s=elem.cancel_orders_s,
                put_val=elem.put_val,
                put_val_b=elem.put_val_b,
                put_val_s=elem.put_val_s,
                put_vol=elem.put_vol,
                put_vol_b=elem.put_vol_b,
                put_vol_s=elem.put_vol_s,
                cancel_val=elem.cancel_val,
                cancel_val_b=elem.cancel_val_b,
                cancel_val_s=elem.cancel_val_s,
                cancel_vol=elem.cancel_vol,
                cancel_vol_b=elem.cancel_vol_b,
                cancel_vol_s=elem.cancel_vol_s,
                put_vwap_b=elem.put_vwap_b,
                put_vwap_s=elem.put_vwap_s,
                cancel_vwap_b=elem.cancel_vwap_b,
                cancel_vwap_s=elem.cancel_vwap_b,
            )
            yield elem.model_dump()
