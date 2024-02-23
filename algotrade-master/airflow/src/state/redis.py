from typing import Any

import orjson
from redis import Redis
from src.core.config import REDIS_CONFIG

from .base import BaseState


class RedisState(BaseState):
    def __init__(self, redis: Redis):
        self.redis = redis

    def get(self, key: str, default_value: str | None = None) -> str | None:
        data = self.redis.get(key)

        if data is None:
            return default_value

        return orjson.loads(data)

    def set(self, key: str, data: Any, expire: int = REDIS_CONFIG.CACHE_EXPIRE) -> None:
        self.redis.set(name=key, value=orjson.dumps(data), ex=expire)
