from sqlalchemy import Column, Integer, String
from database import Base


class Company(Base):
    __tablename__ = "companies"

    ticker = Column(String, primary_key=True)
    name = Column(String)
    icon = Column(String)
    description = Column(String)
    background = Column(String)
    text_color = Column(String)
