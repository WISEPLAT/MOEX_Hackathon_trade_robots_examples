import re
from contextlib import asynccontextmanager, AbstractContextManager
from typing import Callable
from datetime import datetime
from loguru import logger
from asyncio import current_task

from sqlalchemy import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, async_scoped_session, AsyncSession
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ..core.config import POSTGRES


class BaseModel(DeclarativeBase):
    """Базовая модель объекта БД"""

    __abstract__ = True
    __table_args__ = {'schema': POSTGRES.SCHEMA}

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @declared_attr
    def __tablename__(cls):
        """Имя таблицы в базе данных"""

        return re.sub('(?!^)([A-Z][a-z]+)', r'_\1', cls.__name__).lower() + 's'

    def __repr__(self):
        return '<{0.__class__.__name__}(id={0.id!r})>'.format(self)


class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=True)
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                bind=self._engine,
                autoflush=False,
                autocommit=False,
                future=True 
            ),
            scopefunc=current_task
        )

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()
