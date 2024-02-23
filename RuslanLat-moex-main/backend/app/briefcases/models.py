from dataclasses import dataclass
from datetime import datetime
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
class Briefcase:
    id: Optional[int]
    created_at: datetime
    tisker_id: int
    user_id: int
    price: Decimal
    quantity: int
    amount: Decimal


@dataclass
class BriefcaseTotal:
    id: Optional[int]
    tisker_id: int
    user_id: int
    price: Decimal
    quantity: int
    amount: Decimal


@dataclass
class BriefcaseTotalJoin:
    id: Optional[int]
    tisker: str
    name: str
    price: Decimal
    quantity: int
    amount: Decimal


class BriefcaseModel(db):
    __tablename__ = "briefcases"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tisker_id = Column(ForeignKey("tiskers.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    price = Column(Numeric(precision=20, scale=2))
    quantity = Column(Integer)
    amount = Column(Numeric(precision=20, scale=2))
    user = relationship("UserModel", back_populates="briefcase")
    tisker = relationship("TiskerModel", back_populates="briefcase")


class BriefcaseTotalModel(db):
    __tablename__ = "briefcase_totals"
    id = Column(Integer, primary_key=True)
    tisker_id = Column(ForeignKey("tiskers.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    price = Column(Numeric(precision=20, scale=2))
    quantity = Column(Integer)
    amount = Column(Numeric(precision=20, scale=2))
    user = relationship("UserModel", back_populates="briefcase_total")
    tisker = relationship("TiskerModel", back_populates="briefcase_total")
