import typing
from typing import List, Optional
from hashlib import sha256
from sqlalchemy import select, update, and_, delete

from app.users.models import (
    User,
    UserLogin,
    UserModel,
    UserLoginModel,
)
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class UserLoginAccessor(BaseAccessor):
    async def get_by_login(self, login: str) -> Optional[UserLogin]:
        async with self.app.database.session() as session:
            query = select(UserLoginModel).where(UserLoginModel.login == login)
            user: Optional[UserLoginModel] = await session.scalar(query)

        if not user:
            return None

        return UserLogin(
            id=user.id,
            login=user.login,
            password=user.password
        )

    async def create_user_login(
        self, login: str, password: str) -> Optional[UserLogin]:
        new_user: User = UserLoginModel(
            login=login,
            password=self.encode_password(password))

        async with self.app.database.session.begin() as session:
            session.add(new_user)

        return UserLogin(
            id=new_user.id,
            login=new_user.login,
            password=new_user.password)
    
    
    async def update_user_login(self, login: str, password: str) -> Optional[UserLogin]:
        query = (
            update(UserLoginModel)
            .where(UserLoginModel.login == login)
            .values(password=self.encode_password(password))
            .returning(UserLoginModel)
        )

        async with self.app.database.session.begin() as session:
            user = await session.scalar(query)

        if not user:
            return None

        return UserLogin(
            id=user.id,
            login=user.login,
            password=user.password)

    async def delete_user_login(self, login: str) -> Optional[UserLogin]:
        query = delete(UserLoginModel).where(UserLoginModel.login == login).returning(UserLoginModel)

        async with self.app.database.session.begin() as session:
            user = await session.scalar(query)

        if not user:
            return None

        return UserLogin(
            id=user.id,
            login=user.login,
            password=user.password)

    async def list_user_logins(self) -> List[Optional[UserLogin]]:
        query = select(UserLoginModel)

        async with self.app.database.session() as session:
            users = await session.scalars(query)

        if not users:
            return []

        return [
            UserLogin(
            id=user.id,
            login=user.login,
            password=user.password)
            for user in users.all()
        ]

    def encode_password(self, password: str) -> str:
        return sha256(password.encode()).hexdigest()

    def copmare_passwords(self, existing_user: UserLogin, password: str) -> bool:
        return existing_user.password == self.encode_password(password)


class UserAccessor(BaseAccessor):
    async def get_by_id(self, id: int) -> Optional[User]:
        async with self.app.database.session() as session:
            query = select(UserModel).where(UserModel.id == id)
            user: Optional[UserModel] = await session.scalar(query)

        if not user:
            return None

        return User(
            id=user.id,
            name=user.name,
            lastname=user.lastname)

    async def get_by_full_name(self, name: str, lastname: str) -> Optional[User]:
        async with self.app.database.session() as session:
            query = select(UserModel).where(and_(UserModel.name == name, UserModel.lastname == lastname))
            user: Optional[UserModel] = await session.scalar(query)

        if not user:
            return None

        return User(
            id=user.id,
            name=user.name,
            lastname=user.lastname)

    async def create_user(
        self, name: str, lastname: str) -> Optional[User]:
        new_user: User = UserModel(
            name=name,
            lastname=lastname)

        async with self.app.database.session.begin() as session:
            session.add(new_user)

        return User(
            id=new_user.id,
            name=new_user.name,
            lastname=new_user.lastname)
    
    
    async def update_user(self, id: int, name: str, lastname: str) -> Optional[User]:
        query = (
            update(UserModel)
            .where(UserModel.id == id)
            .values(name=name, lastname=lastname)
            .returning(UserModel)
        )

        async with self.app.database.session.begin() as session:
            user = await session.scalar(query)

        if not user:
            return None

        return User(
            id=user.id,
            name=user.name,
            lastname=user.lastname)

    async def delete_user(self, name: str, lastname: str) -> Optional[User]:
        query = delete(UserModel).where(and_(UserModel.name == name, UserModel.lastname==lastname)).returning(UserModel)

        async with self.app.database.session.begin() as session:
            user = await session.scalar(query)

        if not user:
            return None

        return User(
            id=user.id,
            name=user.name,
            lastname=user.lastname)



    async def list_users(self) -> List[Optional[User]]:
        query = select(UserModel)

        async with self.app.database.session() as session:
            users = await session.scalars(query)

        if not users:
            return []

        return [
            User(
            id=user.id,
            name=user.name,
            lastname=user.lastname)
            for user in users.all()
        ]
