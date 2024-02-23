from asyncio import Task
import asyncio
from typing import Optional

from app.store import Store


class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        self.is_running = True
        asyncio.create_task(self.poll(), name="poller_task")

    async def stop(self):
        self.is_running = False
        if self.poll_task:
            await asyncio.wait([self.poll_task], timeout=30)

    async def poll(self):
        while self.is_running:
            updates = await self.store.algopackapi.poll()
            for update in updates:
                tisker = await self.store.tiskers.get_by_tisker(tisker=update.tisker)
                if not await self.store.metrics.get_metric_id(tisker_id=tisker.id):

                    await self.store.metrics.create_metric(
                        tisker_id=tisker.id, value=update.value, delta=update.delta
                    )
                else:
                    await self.store.metrics.update_metric(
                        tisker_id=tisker.id, value=update.value, delta=update.delta
                    )
            await asyncio.sleep(10000)
