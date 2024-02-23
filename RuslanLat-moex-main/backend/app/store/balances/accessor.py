from typing import List, Optional
from decimal import *
from sqlalchemy import select, update, delete

from app.balances.models import Balance, BalanceModel
from app.base.base_accessor import BaseAccessor

getcontext().prec = 2


class BalanceAccessor(BaseAccessor):
    async def get_by_balance_id(self, user_id: int) -> Optional[Balance]:
        async with self.app.database.session() as session:
            query = select(BalanceModel).where(BalanceModel.user_id == user_id)
            balance: Optional[BalanceModel] = await session.scalar(query)

        if not balance:
            return None
        
        return Balance(id=balance.id, user_id=balance.user_id, balance=balance.balance)

    async def create_balance(self, user_id: int, balance: Decimal) -> Optional[Balance]:
        if balance:
            new_balance: BalanceModel = BalanceModel(user_id=user_id, balance=balance)
        else:
            new_balance: BalanceModel = BalanceModel(user_id=user_id)

        async with self.app.database.session.begin() as session:
            session.add(new_balance)

        return Balance(
            id=new_balance.id, user_id=new_balance.user_id, balance=new_balance.balance
        )

    async def update_balance(self, user_id: int, balance: Decimal) -> Optional[Balance]:
        query = (
            update(BalanceModel)
            .where(BalanceModel.user_id == user_id)
            .values(balance=balance)
            .returning(BalanceModel)
        )

        async with self.app.database.session.begin() as session:
            balance: Optional[BalanceModel] = await session.scalar(query)

        if not balance:
            return None

        return Balance(id=balance.id, user_id=balance.user_id, balance=balance.balance)

    async def list_balances(self, user_id: int) -> List[Optional[Balance]]:
        query = select(BalanceModel)

        if user_id:
            query = query.where(BalanceModel.user_id==user_id)

        async with self.app.database.session() as session:
            balances = await session.scalars(query)

        if not balances:
            return []

        return [
            Balance(id=balance.id, user_id=balance.user_id, balance=balance.balance)
            for balance in balances.all()
        ]
