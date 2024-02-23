import asyncio
import os
from datetime import timedelta
from tinkoff.invest import AsyncClient, CandleInterval
from tinkoff.invest.schemas import MarketDataRequest, Quotation

TOKEN = 't.ZsrYdAC-An0uyHnudfvRJ2MVp39P77b7I7MNsCa3p5zPFpi0xbvLraeMSjQEAdwXN4xaSlCE-w_M6kWlsMpKkA'

class AsyncMarketDataStreamManager:
    def __init__(self, market_data_stream):
        self._market_data_stream_service = market_data_stream
        self._market_data_stream = None
        self._requests = asyncio.Queue()
        self._unsubscribe_event = asyncio.Event()

    async def _get_request_generator(self):
        while not self._unsubscribe_event.is_set() or not self._requests.empty():
            try:
                request = await asyncio.wait_for(self._requests.get(), timeout=1.0)
            except asyncio.exceptions.TimeoutError:
                pass
            else:
                yield request
                self._requests.task_done()

    @property
    def last_price(self):
        return LastPriceStream(parent_manager=self)

    def subscribe(self, market_data_request):
        self._requests.put_nowait(market_data_request)

    def unsubscribe(self, market_data_request):
        self._requests.put_nowait(market_data_request)

    def stop(self):
        self._unsubscribe_event.set()

    def __aiter__(self):
        self._unsubscribe_event.clear()
        self._market_data_stream = (
            self._market_data_stream_service.create_market_data_stream(
                self._get_request_generator()
            )
        ).__aiter__()

        return self

    async def __anext__(self):
        return await self._market_data_stream.__anext__()

# Assuming Quotation is used for representing last prices
class LastPriceStream:
    def __init__(self, parent_manager):
        self.parent_manager = parent_manager
        self.payload = Quotation(units=0, nano=0)
async def main():
    async with AsyncClient(TOKEN) as client:
        async_market_data_stream_manager = AsyncMarketDataStreamManager(
            market_data_stream=client
        )

        # Subscribe to last price stream
        async_market_data_stream_manager.subscribe(
            MarketDataRequest(
                figi="BBG004730N88",
                depth=1,  # Depth is set to 1 to get only the last price
                interval=CandleInterval.CANDLE_INTERVAL_HOUR,  # Adjust with the correct interval
            )
        )

        # Iterate over the stream to get the last price
        async for response in async_market_data_stream_manager:
            if isinstance(response, LastPriceStream):
                print("Last Price:", response.payload)

        # Stop the market data stream manager when done
        async_market_data_stream_manager.stop()

if __name__ == "__main__":
    asyncio.run(main())
