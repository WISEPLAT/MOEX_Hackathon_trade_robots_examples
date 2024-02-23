import asyncio
import typing
from typing import Optional

from aiohttp.client import ClientSession
from aiohttp import TCPConnector
from datetime import datetime, timedelta

from app.base.base_accessor import BaseAccessor
from app.store.algopackapi.dataclasses import MetricData, Candles, CandleData
from app.store.algopackapi.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AlgoPackApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.poller: Optional[Poller] = None

    async def connect(self, app: "Application"):
        self.session = ClientSession()
        self.poller = Poller(app.store)
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.session:
            await self.session.close()
        if self.poller:
            await self.poller.stop()

    @staticmethod
    def _build_query_metric(tisker: str) -> str:
        url = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{tisker}.json"

        return url

    @staticmethod
    def _build_query_candles(tisker: str) -> str:
        current_date = datetime.now().date()
        last_date = str(current_date - timedelta(days=30 * 21))

        url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{tisker}/candles.xml?from={last_date}&till={current_date}&interval=24"

        return url

    async def get_metric_data(self, tisker: str) -> MetricData:
        query = self._build_query_metric(tisker=tisker)

        async with self.session.get(query) as response:
            data = await response.json()
            metric_data = data["marketdata"]["data"][0]
            metric_columns = data["marketdata"]["columns"]
            if metric_data[metric_columns.index("LCURRENTPRICE")]:
                value = metric_data[metric_columns.index("LCURRENTPRICE")]
                delta = metric_data[metric_columns.index("WAPTOPREVWAPRICE")]
            else:
                value = metric_data[metric_columns.index("MARKETPRICE")]
                delta = 0.00

        return MetricData(tisker=tisker, value=float(value), delta=float(delta))

    async def get_candles_data(self, tisker: str) -> MetricData:
        query = self._build_query_candles(tisker=tisker)

        async with self.session.get(query) as response:
            data = await response.json()
            candle_datas = data["candles"]["data"][0]
            candle_columns = data["candles"]["columns"]

        for candle in candle_datas:
            candle_data = CandleData(
                tisker=tisker,
                open=candle[0],
                close=candle[1],
                high=candle[2],
                low=candle[3],
                day=candle[-1],
            )



    async def poll(self):
        self.logger.info("get metric data")
        tiskers = await self.app.store.tiskers.list_tiskers()
        tasks = [
            asyncio.create_task(self.get_metric_data(tisker.tisker))
            for tisker in tiskers
        ]
        updates = await asyncio.gather(*tasks)

        return updates
