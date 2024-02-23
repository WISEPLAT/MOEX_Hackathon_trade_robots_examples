from datetime import datetime

from src.models.base import JSONModel, UUIDMixin, CreatedModelMixin


class CandleModel(JSONModel, UUIDMixin, CreatedModelMixin):
    secid: str
    open: float
    close: float
    high: float
    low: float
    value: float
    volume: int
    begin: datetime
    end: datetime
