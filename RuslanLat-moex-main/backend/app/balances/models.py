from dataclasses import dataclass
from decimal import *
from typing import Optional
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    DateTime,
    Numeric
)
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db

getcontext().prec = 2

@dataclass
class Balance:
    id: Optional[int]
    user_id: int
    balance: Decimal


class BalanceModel(db):
    __tablename__ = "balances"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    balance = Column(Numeric(precision=20, scale=2), default=1000000.00)
    user = relationship("UserModel", back_populates="balance")
