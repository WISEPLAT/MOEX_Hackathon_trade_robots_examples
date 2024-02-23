from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base


class Bot(Base):
    __tablename__ = "bots_states"

    user_id = Column(Integer, primary_key=True, unique=True, index=True)
    state = Column(Integer)
    date_to = Column(String)
    risk_level = Column(Integer)
    initial_balance = Column(Integer)
    current_balance = Column(Integer)
