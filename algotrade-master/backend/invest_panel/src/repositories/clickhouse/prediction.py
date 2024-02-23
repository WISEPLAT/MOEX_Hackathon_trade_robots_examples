from typing import Iterator, Any
from datetime import datetime

from .base import BaseRepository


class PredictionRepository(BaseRepository):
    table = 'default.predictions'

    def time_series(
        self,
        *,
        fields: list[str],
        ts: datetime | None = None,
        till_ts: datetime | None = None,
        secid: str | None = None,
        order_by: dict[str, str] | None = None,
        group_by: dict[str, str] | None = None,
        limit: int = 100000,
        **kwargs
    ) -> Iterator[Any]:
        
        where = []

        if secid is not None:
            where.append(f"secid = '{secid}'")

        if ts is not None:
            where.append(f"timestamp >= '{ts.isoformat()}'")

        if till_ts is not None:
            where.append(f"timestamp <= '{till_ts.isoformat()}'")

        return super().time_series(
            fields=fields,
            where=where,
            secid=secid,
            order_by=order_by,
            group_by=group_by,
            limit=limit,
            **kwargs
        )
