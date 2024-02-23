import orjson
import uuid

from datetime import datetime
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class JSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        use_enum_values = True


class UUIDMixin(BaseModel):
    id: uuid.UUID | None = Field(default_factory=lambda: uuid.uuid4())


class CreatedModelMixin(BaseModel):
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)


class TimestampMixin(CreatedModelMixin):
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
