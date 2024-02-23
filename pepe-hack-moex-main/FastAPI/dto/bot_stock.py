from pydantic import BaseModel


class BotStocks(BaseModel):
    user_id: int
    company_name: str
    stocks_count: int | None = None
    purchase_price: float | None = None
    current_price: float | None = None
