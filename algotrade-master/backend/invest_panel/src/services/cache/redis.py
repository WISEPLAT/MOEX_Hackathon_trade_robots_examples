from typing import Any

import orjson
from redis.asyncio import Redis
from src.core.config import REDIS_CONFIG

from .base import BaseCache


class RedisCache(BaseCache):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str, default_value: str | None = None) -> str | None:
        data = await self.redis.get(key)

        if data is None:
            return default_value

        return orjson.loads(data)

    async def set(self, key: str, data: Any, expire: int = REDIS_CONFIG.CACHE_EXPIRE) -> None:
        await self.redis.set(name=key, value=orjson.dumps(data), ex=expire)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)
