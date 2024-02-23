from datetime import datetime

from src.models.base import JSONModel, UUIDMixin, CreatedModelMixin


class OrderstatModel(JSONModel, UUIDMixin, CreatedModelMixin):
    secid: str
    ts: datetime
    put_orders: int | None
    put_orders_b: int | None
    put_orders_s: int | None
    cancel_orders: int | None
    cancel_orders_b: int | None
    cancel_orders_s: int | None
    put_vol: int | None
    put_vol_b: int | None
    put_vol_s: int | None
    cancel_vol: int | None
    cancel_vol_b: int | None
    cancel_vol_s: int | None
    put_val: float | None
    put_val_b: float | None
    put_val_s: float | None
    cancel_val: float | None
    cancel_val_b: float | None
    cancel_val_s: float | None
    put_vwap_b: float | None
    put_vwap_s: float | None
    cancel_vwap_b: float | None
    cancel_vwap_s: float | None
    