from dependency_injector import containers, providers

from .base import BaseContainer
from src.services.trades.prediction import PredictionService
from src.repositories.clickhouse.prediction import PredictionRepository
from src.core.config import NODES


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..api.v1.trades'])

    config = providers.Configuration()

    prediction_repository = providers.Factory(
        PredictionRepository,
        host=NODES[0].HOST,
        port=NODES[0].PORT,
        user=NODES[0].USER,
        password=NODES[0].PASSWORD,
        alt_hosts=[','.join(f"{NODE.HOST}:{NODE.PORT}") for NODE in NODES[1:]]
    )

    prediction_service = providers.Factory(
        PredictionService,
        trade_repository=prediction_repository,
    )
