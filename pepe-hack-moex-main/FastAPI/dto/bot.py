from pydantic import BaseModel
from enum import IntEnum


class BotState(IntEnum):
    OFF = 0
    ON = 1


class Bot(BaseModel):
    user_id: int
    state: BotState
    date_to: str | None = None
    risk_level: int | None = None
    initial_balance: int | None = None
    current_balance: int | None = None
