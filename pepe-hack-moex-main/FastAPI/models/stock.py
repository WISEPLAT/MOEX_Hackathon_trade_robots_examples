from sqlalchemy import Column, String, Float, ForeignKey
from database import Base


class Stock(Base):
    __tablename__ = "stocks"

    ticker = Column(String, ForeignKey("companies.ticker"), primary_key=True)
    price = Column(Float)
    price_increase = Column(Float)
