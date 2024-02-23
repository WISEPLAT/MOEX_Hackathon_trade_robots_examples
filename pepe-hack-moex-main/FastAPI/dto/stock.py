from pydantic import BaseModel
from enum import IntEnum


class StocksType(IntEnum):
    RISING = 0
    FALLING = 1
    ADVISED = 2


class Stock(BaseModel):
    ticker: str
    price: float
    price_increase: float
