from decimal import *
from typing import List, Optional
from sqlalchemy import func, select, update, delete, and_
from sqlalchemy.orm import joinedload, join

from app.briefcases.models import (
    Briefcase,
    BriefcaseModel,
    BriefcaseTotal,
    BriefcaseTotalModel,
    BriefcaseTotalJoin,
)
from app.tiskers.models import TiskerModel
from app.base.base_accessor import BaseAccessor

getcontext().prec = 2


class BriefcaseAccessor(BaseAccessor):
    async def create_briefcase(
        self,
        tisker_id: int,
        user_id: int,
        price: Decimal,
        quantity: int,
        amount: Decimal,
    ) -> Optional[Briefcase]:
        new_briefcase: Briefcase = BriefcaseModel(
            tisker_id=tisker_id,
            user_id=user_id,
            price=price,
            quantity=quantity,
            amount=amount,
        )
        async with self.app.database.session.begin() as session:
            session.add(new_briefcase)

        return Briefcase(
            id=new_briefcase.id,
            created_at=new_briefcase.created_at,
            tisker_id=new_briefcase.tisker_id,
            user_id=new_briefcase.user_id,
            price=new_briefcase.price,
            quantity=new_briefcase.quantity,
            amount=new_briefcase.amount,
        )

    async def list_briefcases(self, user_id: int) -> List[Optional[Briefcase]]:
        query = select(BriefcaseModel)

        if user_id:
            query = query.where(BriefcaseModel.user_id == user_id)

        async with self.app.database.session() as session:
            briefcases: List[Optional[BriefcaseModel]] = await session.scalars(query)

        if not briefcases:
            return []

        return [
            Briefcase(
                id=briefcase.id,
                created_at=briefcase.created_at,
                tisker_id=briefcase.tisker_id,
                user_id=briefcase.user_id,
                price=briefcase.price,
                quantity=briefcase.quantity,
                amount=briefcase.amount,
            )
            for briefcase in briefcases.all()
        ]

    async def list_briefcases_join(
        self, user_id: int
    ) -> List[Optional[BriefcaseTotalJoin]]:
        query = select(BriefcaseModel).options(joinedload(BriefcaseModel.tisker))

        if user_id:
            query = query.where(BriefcaseModel.user_id == user_id)

        async with self.app.database.session() as session:
            briefcases = await session.scalars(query)

        if not briefcases:
            return []
        return [
            BriefcaseTotalJoin(
                id=briefcase.id,
                tisker=briefcase.tisker.tisker,
                name=briefcase.tisker.name,
                price=briefcase.price,
                quantity=briefcase.quantity,
                amount=briefcase.amount,
            )
            for briefcase in briefcases.all()
        ]

    async def create_briefcase_total(
        self,
        tisker_id: int,
        user_id: int,
        price: Decimal,
        quantity: int,
        amount: Decimal,
    ) -> Optional[Briefcase]:
        new_briefcase: BriefcaseTotal = BriefcaseTotalModel(
            tisker_id=tisker_id,
            user_id=user_id,
            price=price,
            quantity=quantity,
            amount=amount,
        )

        async with self.app.database.session.begin() as session:
            session.add(new_briefcase)

        return BriefcaseTotal(
            id=new_briefcase.id,
            tisker_id=new_briefcase.tisker_id,
            user_id=new_briefcase.user_id,
            price=new_briefcase.price,
            quantity=new_briefcase.quantity,
            amount=new_briefcase.amount,
        )

    async def get_by_briefcase_id(self, user_id: int) -> Optional[BriefcaseTotal]:
        async with self.app.database.session() as session:
            query = select(BriefcaseTotalModel).where(
                BriefcaseTotalModel.user_id == user_id
            )
            briefcase: Optional[BriefcaseTotalModel] = await session.scalar(query)

        if not briefcase:
            return None
        return BriefcaseTotal(
            id=briefcase.id,
            tisker_id=briefcase.tisker_id,
            user_id=briefcase.user_id,
            price=briefcase.price,
            quantity=briefcase.quantity,
            amount=briefcase.amount,
        )

    async def update_briefcase(
        self,
        tisker_id: int,
        user_id: int,
        price: Decimal,
        quantity: int,
        amount: Decimal,
    ) -> Optional[BriefcaseTotal]:
        query = (
            update(BriefcaseTotalModel)
            .where(
                and_(
                    BriefcaseTotalModel.user_id == user_id,
                    BriefcaseTotalModel.tisker_id == tisker_id,
                )
            )
            .values(price=price, quantity=quantity, amount=amount)
            .returning(BriefcaseTotalModel)
        )

        async with self.app.database.session.begin() as session:
            briefcase: Optional[BriefcaseTotalModel] = await session.scalar(query)

        if not briefcase:
            return None

        return BriefcaseTotal(
            id=briefcase.id,
            tisker_id=briefcase.tisker_id,
            user_id=briefcase.user_id,
            price=briefcase.price,
            quantity=briefcase.quantity,
            amount=briefcase.amount,
        )

    async def list_briefcase_totals(
        self, user_id: int
    ) -> List[Optional[BriefcaseTotal]]:
        query = select(BriefcaseTotalModel)

        if user_id:
            query = query.where(BriefcaseTotalModel.user_id == user_id)

        async with self.app.database.session() as session:
            briefcases: List[Optional[BriefcaseTotalModel]] = await session.scalars(
                query
            )

        if not briefcases:
            return []

        return [
            BriefcaseTotal(
                id=briefcase.id,
                tisker_id=briefcase.tisker_id,
                user_id=briefcase.user_id,
                price=briefcase.price,
                quantity=briefcase.quantity,
                amount=briefcase.amount,
            )
            for briefcase in briefcases.all()
        ]

    async def list_briefcase_totals_join(
        self, user_id: int
    ) -> List[Optional[BriefcaseTotalJoin]]:
        query = select(BriefcaseTotalModel).options(
            joinedload(BriefcaseTotalModel.tisker)
        )

        if user_id:
            query = query.where(BriefcaseTotalModel.user_id == user_id)

        async with self.app.database.session() as session:
            briefcases = await session.scalars(query)

        if not briefcases:
            return []

        return [
            BriefcaseTotalJoin(
                id=briefcase.id,
                tisker=briefcase.tisker.tisker,
                name=briefcase.tisker.name,
                price=briefcase.price,
                quantity=briefcase.quantity,
                amount=briefcase.amount,
            )
            for briefcase in briefcases.all()
        ]
