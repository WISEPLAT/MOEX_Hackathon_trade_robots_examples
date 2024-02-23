from typing import Optional, Type

from dependency_injector import providers, resources

from src.services.cache.redis import RedisCache
from src.services.cache.base import BaseCache
from src.instances.redis import get_redis


class CacheResource(providers.Resource):
    provided_type: Optional[Type] = BaseCache


class RedisCacheResource(resources.AsyncResource):
    async def init(self, *args, **kwargs) -> BaseCache:
        redis = await get_redis()
        return RedisCache(redis=redis)
