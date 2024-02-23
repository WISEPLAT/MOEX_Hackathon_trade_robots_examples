from datetime import datetime

from src.models.base import JSONModel


class PredictionTS(JSONModel):
    secid: str
    value: float
    algorithm: str
    timestamp: datetime
