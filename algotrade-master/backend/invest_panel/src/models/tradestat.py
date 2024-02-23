from datetime import datetime

from src.models.base import JSONModel, UUIDMixin, CreatedModelMixin


class Tradestat(JSONModel, UUIDMixin, CreatedModelMixin):
    secid: str
    ts: datetime
    pr_open: float
    pr_high: float
    pr_low: float
    pr_close: float
    pr_change: float
    trades: int | None
    trades_b: int | None
    trades_s: int | None
    vol: int | None
    vol_b: int | None
    vol_s: int | None
    val: float | None
    val_b: float | None
    val_s: float | None
    pr_std: float | None
    disb: float | None
    pr_vwap: float | None
    pr_vwap_b: float | None
    pr_vwap_s: float | None
