from typing import Any, Optional, TYPE_CHECKING
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.url import URL

from app.store.database.sqlalchemy_base import db

if TYPE_CHECKING:
    from app.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app: "Application" = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[async_sessionmaker[AsyncSession]] = None

    async def connect(self, *_: list, **__: dict) -> None:
        self._db: declarative_base = db
        self._engine: AsyncEngine = create_async_engine(
            URL.create(
                drivername="postgresql+asyncpg",
                host=self.app.config.database.host,
                database=self.app.config.database.database,
                username=self.app.config.database.user,
                password=self.app.config.database.password,
                port=self.app.config.database.port,
            )
        )
        self.session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            autoflush=True,
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def disconnect(self, *_: Any, **__: Any) -> None:
        try:
            await self._engine.dispose()
        except:
            pass
