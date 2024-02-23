import typing
from typing import List, Optional
from sqlalchemy import select, update, delete

from app.tiskers.models import Tisker, TiskerModel
from app.base.base_accessor import BaseAccessor


class TiskerAccessor(BaseAccessor):
    async def get_by_tisker(self, tisker: str) -> Optional[Tisker]:
        async with self.app.database.session() as session:
            query = select(TiskerModel).where(TiskerModel.tisker == tisker)
            tisker: Optional[TiskerModel] = await session.scalar(query)
        if not tisker:
            return None

        return Tisker(id=tisker.id, tisker=tisker.tisker, name=tisker.name)

    async def get_by_tisker_id(self, id: int) -> Optional[Tisker]:
        async with self.app.database.session() as session:
            query = select(TiskerModel).where(TiskerModel.id == id)
            tisker: Optional[TiskerModel] = await session.scalar(query)

        if not tisker:
            return None

        return Tisker(id=tisker.id, tisker=tisker.tisker, name=tisker.name)

    async def create_tisker(self, tisker: str, name: str) -> Optional[Tisker]:
        new_tisker: TiskerModel = TiskerModel(tisker=tisker, name=name)

        async with self.app.database.session.begin() as session:
            session.add(new_tisker)

        return Tisker(id=new_tisker.id, tisker=new_tisker.tisker, name=new_tisker.name)

    async def update_tisker(self, id: int, tisker: str, name: str) -> Optional[Tisker]:
        query = (
            update(TiskerModel)
            .where(TiskerModel.id == id)
            .values(tisker=tisker, name=name)
            .returning(TiskerModel)
        )

        async with self.app.database.session.begin() as session:
            tisker: Optional[TiskerModel] = await session.scalar(query)

        if not tisker:
            return None

        return Tisker(id=tisker.id, tisker=tisker.tisker, name=tisker.name)

    async def delete_tisker(self, tisker: str) -> Optional[Tisker]:
        query = delete(TiskerModel).where(TiskerModel.tisker == tisker).returning(TiskerModel)

        async with self.app.database.session.begin() as session:
            tisker: Optional[TiskerModel] = await session.scalar(query)

        if not tisker:
            return None

        return Tisker(id=tisker.id, tisker=tisker.tisker, name=tisker.name)

    async def list_tiskers(self) -> List[Optional[Tisker]]:
        query = select(TiskerModel)

        async with self.app.database.session() as session:
            tiskers: List[Optional[TiskerModel]] = await session.scalars(query)

        if not tiskers:
            return []

        return [Tisker(id=tisker.id, tisker=tisker.tisker, name=tisker.name) for tisker in tiskers.all()]