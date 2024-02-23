from dataclasses import dataclass
from hashlib import sha256
from typing import Optional
from sqlalchemy import Column, Integer, String

from app.store.database.sqlalchemy_base import db


@dataclass
class Admin:
    id: int
    login: str
    password: Optional[str] = None

    def is_password_valid(self, password: str) -> bool:
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["Admin"]:
        return cls(id=session["admin"]["id"], login=session["admin"]["login"])


class AdminModel(db):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
