from dataclasses import dataclass
import datetime
from decimal import Decimal

@dataclass
class MetricData:
    tisker: str
    value: Decimal
    delta: Decimal


@dataclass
class CandleData:
    tisker: str
    open: Decimal
    close: Decimal
    high: Decimal
    low: Decimal 
    day: datetime


@dataclass
class Candles:
    candles: CandleData