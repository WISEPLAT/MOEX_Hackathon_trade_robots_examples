from sqlalchemy import Column, Integer, Float, String, ForeignKey, PrimaryKeyConstraint
from database import Base


class Forecast(Base):
    __tablename__ = "forecasts"

    ticker = Column(Integer, ForeignKey("companies.ticker"))
    period = Column(String)
    price = Column(Float)
    price_increase = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(period, ticker),
        {},
    )
