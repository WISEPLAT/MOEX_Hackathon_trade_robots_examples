from datetime import datetime

from src.models.base import JSONModel, UUIDMixin, CreatedModelMixin


class OBstat(JSONModel, UUIDMixin, CreatedModelMixin):
    secid: str
    ts: datetime
    spread_bbo: float | None
    spread_lv10: float | None
    spread_1mio: float | None
    levels_b: int | None
    levels_s: int | None
    vol_b: int | None
    vol_s: int | None
    val_b: float | None
    val_s: float | None
    imbalance_vol_bbo: float | None
    imbalance_val_bbo: float | None
    imbalance_vol: float | None
    imbalance_val: float | None
    vwap_b: float | None
    vwap_s: float | None
    vwap_b_1mio: float | None
    vwap_s_1mio: float | None
