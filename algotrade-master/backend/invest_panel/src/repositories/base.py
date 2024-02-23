from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.base import BaseModel


class BaseRepository(ABC):

    @property
    @abstractmethod
    def model(self):
        """Модель БД"""

    @property
    @abstractmethod
    def schema(self):
        """Pydantic model"""

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    async def all(self) -> Iterator[BaseModel]:
        async with self.session_factory() as session:
            query = select(self.model)
            entities = await session.scalars(query)
            return entities.all()
        
    async def get(self, **kwargs) -> BaseModel:
        query = select(self.model)

        for key, value in kwargs.items():
            query = query.filter(getattr(self.model, key) == value)

        async with self.session_factory() as session:
            entity = await session.execute(query)
            return entity.scalar()

    async def one(self, **kwargs) -> BaseModel:
        entity = await self.get(**kwargs)
        
        if not entity:
            raise ValueError(f"Etity not found, '{kwargs}'")
        
        return entity
