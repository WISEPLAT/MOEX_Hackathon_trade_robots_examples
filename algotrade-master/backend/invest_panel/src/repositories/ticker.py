from .base import BaseRepository
from ..db.ticker import Ticker
from src.models.ticker import Ticker as TickerModel


class TickerRepository(BaseRepository):
    model = Ticker
    schema = TickerModel
