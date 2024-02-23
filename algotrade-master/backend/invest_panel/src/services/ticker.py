from ..repositories.base import BaseRepository
from ..db.ticker import Ticker


class TickerService:

    def __init__(self, ticker_repository: BaseRepository) -> None:
        self._repository: BaseRepository = ticker_repository

    async def get(self, secid: str, **kwargs) -> Ticker:
        return await self._repository.get(secid=secid, **kwargs)
    
    async def one(self, secid: str, **kwargs) -> Ticker:
        return await self._repository.one(secid=secid, **kwargs)
    
    async def all(self, **kwargs) -> Ticker:
        return await self._repository.all(**kwargs)
