from pydantic import BaseModel


class Company(BaseModel):
    ticker: str
    name: str
    icon: str
    description: str
    background: str
    text_color: str
