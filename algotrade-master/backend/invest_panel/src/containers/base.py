from dependency_injector import containers, providers

from ..services.cache.base import BaseCache


class BaseContainer(containers.DeclarativeContainer):
    cache_svc = providers.Dependency(instance_of=BaseCache)
