import typing
from typing import Optional
from hashlib import sha256
from sqlalchemy import select

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor


class AdminAccessor(BaseAccessor):
    async def get_by_login(self, login: str) -> Optional[Admin]:
        async with self.app.database.session() as session:
            query = select(AdminModel).where(AdminModel.login == login)
            admin: Optional[AdminModel] = await session.scalar(query)

        if not admin:
            return None

        return Admin(id=admin.id, login=admin.login, password=admin.password)

    async def create_admin(self, login: str, password: str) -> Optional[Admin]:
        new_admin: Admin = AdminModel(
            login=login, password=self.encode_password(password)
        )

        async with self.app.database.session() as session:
            session.add(new_admin)

        return Admin(id=new_admin.id, login=new_admin.login)

    def encode_password(self, password: str) -> str:
        return sha256(password.encode()).hexdigest()

    def copmare_passwords(self, existing_admin: Admin, password: str) -> bool:
        return existing_admin.password == self.encode_password(password)
