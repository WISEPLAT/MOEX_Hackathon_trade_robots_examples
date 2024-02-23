from pydantic import BaseModel


class NewsResponse(BaseModel):
    id: int
    title: str
    description: str


class DetailedNewsResponse(NewsResponse):
    text: str
