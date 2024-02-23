from sqlalchemy import Column, Integer, String, Float
from database import Base


class BotAction(Base):
    __tablename__ = "bot_actions"

    action_id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    user_id = Column(Integer, index=True)
    company_name = Column(String)
    stocks_count = Column(Integer)
    action = Column(String)
    action_color = Column(String)
    profit = Column(Float)
    comment = Column(String)
    datetime = Column(String)
