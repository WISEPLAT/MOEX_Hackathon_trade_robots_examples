import orjson
import enum
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, validator
from typing import TypeVar, Generic, Any
from fastapi import Query

from src.core.config import CONFIG


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class JSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        use_enum_values = True


class UUIDMixin(BaseModel):
    id: UUID | None = Field(default_factory=lambda: uuid4())


class CreatedModelMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TimestampMixin(CreatedModelMixin):
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class StrEnum(str, enum.Enum):
    @classmethod
    def find_elem(cls, value: Any) -> enum.Enum | None:
        for e in cls:
            if e.value == value:
                return e
        return None


class IntervalEnum(StrEnum):
    HOUR = 'hour'
    MINUTE = 'minute'


class Interval(JSONModel):
    interval: str

    @validator('interval')
    def interval_validate(value: str) -> str:
        try:
            _, interval_type = value.split()
        except:
            raise ValueError("Bad interval")

        if IntervalEnum.find_elem(interval_type) is None:
            raise ValueError("Bad interval type")

        return value


# PTYPE = TypeVar('PTYPE', bound=BaseModel)


# class PageModel(JSONModel, Generic[PTYPE]):

#     next_page: int | None = Field(title='Номер следующей страницы', example=3)
#     prev_page: int | None = Field(title='Номер предыдущей страницы', example=1)
#     page: int | None = Field(default=CONFIG.APP.PAGE, title='Номер текущей страницы', example=2)
#     page_size: int | None = Field(default=CONFIG.APP.PAGE_SIZE, title='Длина выборки', example=2)
#     total: int | None = Field(default=0, title='Общая мощность выборки', example=1000)
#     items: list[PTYPE] = Field(default=[], title='Список объектов', example=[])


# class Paginator(BaseModel):
#     page: int = Query(default=CONFIG.APP.page, title='Номер текущей страницы', ge=1)
#     page_size: int = Query(default=CONFIG.APP.page_size, title='Длина выборки', ge=1, le=500)