from dependency_injector import containers, providers

from .base import BaseContainer
from src.services.trades.candle import CandleService
from src.repositories.clickhouse.candle import CandleRepository
from src.core.config import NODES


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..api.v1.trades'])

    config = providers.Configuration()

    candle_repository = providers.Factory(
        CandleRepository,
        host=NODES[0].HOST,
        port=NODES[0].PORT,
        user=NODES[0].USER,
        password=NODES[0].PASSWORD,
        alt_hosts=[','.join(f"{NODE.HOST}:{NODE.PORT}") for NODE in NODES[1:]]
    )

    candle_service = providers.Factory(
        CandleService,
        trade_repository=candle_repository,
    )
