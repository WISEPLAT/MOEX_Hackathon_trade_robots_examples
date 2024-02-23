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
class Metric:
    id: Optional[int]
    tisker_id: int
    value: Decimal
    delta: Decimal


@dataclass
class MetricTotalJoin:
    id: Optional[int]
    tisker: str
    name: str
    value: Decimal
    delta: Decimal


class MetricModel(db):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True)
    tisker_id = Column(ForeignKey("tiskers.id", ondelete="CASCADE"), unique=True, nullable=False)
    value = Column(Numeric(precision=20, scale=2))
    delta = Column(Numeric(precision=20, scale=2))
    tisker = relationship("TiskerModel", back_populates="metric")
