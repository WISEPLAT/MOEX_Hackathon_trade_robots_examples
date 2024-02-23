from pydantic import BaseModel
from enum import Enum


class ForecastPeriod(Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"


class Forecast(BaseModel):
    ticker: str
    period: ForecastPeriod
    price: float
    price_increase: float
