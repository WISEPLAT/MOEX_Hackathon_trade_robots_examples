from dependency_injector import containers, providers

from ..db.base import Database
from .base import BaseContainer
from ..services.ticker import TickerService
from ..repositories.ticker import TickerRepository


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..api.v1.ticker'])

    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=config.db.url)

    ticker_repository = providers.Factory(
        TickerRepository,
        session_factory=db.provided.session,
    )

    ticker_service = providers.Factory(
        TickerService,
        ticker_repository=ticker_repository,
    )
