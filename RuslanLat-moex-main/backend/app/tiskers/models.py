from dataclasses import dataclass
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db



@dataclass
class Tisker:
    id: Optional[int]
    tisker: str
    name: str


class TiskerModel(db):
    __tablename__ = "tiskers"
    id = Column(Integer, primary_key=True)
    tisker = Column(String, unique=True)
    name = Column(String)
    briefcase = relationship("BriefcaseModel", back_populates="tisker")
    briefcase_total = relationship("BriefcaseTotalModel", back_populates="tisker")
    metric = relationship("MetricModel", back_populates="tisker")