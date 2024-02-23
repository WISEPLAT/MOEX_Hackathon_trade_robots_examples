from datetime import datetime

from src.models.base import JSONModel, UUIDMixin, CreatedModelMixin


class PredictionModel(JSONModel, UUIDMixin, CreatedModelMixin):
    secid: str
    algorithm: str
    value: float
    timestamp: datetime
