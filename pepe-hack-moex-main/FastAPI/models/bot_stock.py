from sqlalchemy import Column, Integer, String, Float, PrimaryKeyConstraint
from database import Base


class BotStocks(Base):
    __tablename__ = "bot_stocks"

    user_id = Column(Integer, index=True)
    company_name = Column(String)
    stocks_count = Column(Integer)
    purchase_price = Column(Float)
    current_price = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(company_name, user_id),
        {},
    )
