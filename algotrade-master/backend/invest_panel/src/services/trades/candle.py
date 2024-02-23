from datetime import datetime
from typing import Iterator, Any

from src.repositories.clickhouse.base import BaseRepository
from src.models.candle import CandleTS


class CandleService:

    def __init__(self, trade_repository: BaseRepository) -> None:
        self._repository: BaseRepository = trade_repository

    async def get_time_series(
        self,
        *,
        fields: list[str] | None = None,
        secid: str | None = None,
        interval: str | None = None,
        ts: datetime | None = None,
        till_ts: datetime | None = None,
        group_by: list[str] | None = None,
        order_by: dict[str, str] | None = None,
        limit: int = 100000,
        **kwargs
    ) -> Iterator[dict[str, Any]]:
        
        raw_ts_gen = self._repository.time_series(
            secid=secid,
            fields=fields or ['*'],
            interval=interval,
            ts=ts,
            till_ts=till_ts,
            group_by=group_by,
            order_by=order_by,
            limit=limit,
            **kwargs
        )

        for elem in raw_ts_gen:
            yield CandleTS(
                secid=elem.get('secid'),
                open=elem.get('open'),
                close=elem.get('close'),
                low=elem.get('low'),
                high=elem.get('high'),
                volume=elem.get('volume'),
                value=elem.get('value'),
                ts=elem.get('begin'),
            )
