import datetime
from enum import Enum

from pydantic import BaseModel


class Period(str, Enum):
    one_minute = '1m'
    ten_minutes = '10m'
    one_hour = '1h'
    one_day = 'D'
    one_week = 'W'
    one_month = 'M'
    one_quarter = 'Q'


class TickerCandleResponse(BaseModel):
    begin: datetime.datetime
    end: datetime.datetime
    close: float


class TickerPriceRequest(BaseModel):
    period: Period
    date_start: datetime.date
    date_end: datetime.date


class TickerResponse(BaseModel):
    ticker: str
    sphere: str
    price: float
    name: str
    is_positive_forecast: bool


class RelevantTickerResponse(TickerResponse):
    correlation_score: float

