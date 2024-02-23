import enum
import uuid
from pydantic import Field, validator
from datetime import datetime
from typing import Any
from random import randint

from models.base import JSONModel


NAMESPACE_ID = uuid.UUID("6ba7b816-9dad-11d1-80b4-00c04fd430c8")


class EventType(str, enum.Enum):
    STARTING = "starting"
    STOPPED = "stopped"
    VIEWED = "viewed"


class MovieFrameDatagram(JSONModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    movie_id: str
    frame_time: int
    movie_duration: int
    event_type: EventType = Field(default=EventType.VIEWED)
    event_timestamp: int = Field(
        default_factory=lambda: int(datetime.utcnow().timestamp())
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("user_id", "movie_id")
    def valid_uuid(value: str):
        try:
            uuid.UUID(value)
            return value
        except ValueError:
            return str(uuid.uuid5(namespace=NAMESPACE_ID, name=value))

    @validator("movie_duration", "frame_time")
    def frame_time_ge_zero(cls, value: int) -> int:
        if value >= 0:
            return value

        raise ValueError('"frame_time" and "movie_duration" must be greater than zero')

    @validator("movie_duration")
    def movie_duration_ge_frame_time(
        cls, value: int, values: dict[str, Any], **kwargs
    ) -> int:
        if values.get("frame_time") is not None and value >= values.get("frame_time"):
            return value

        raise ValueError('"movie_duration" must be greater than "frame_time"')


class MovieRating(JSONModel):
    rating: float
    duration: int = Field(default_factory=lambda: randint(1, 3) * 60 * 60 * 60)

    @validator("rating")
    def rating_ge_zero(cls, value: float) -> float:
        return value / 10 if value > 0 else 0

    @property
    def start(self) -> int:
        return randint(0, 10) * 60

    @property
    def stop(self) -> int:
        return self.rating * self.duration + self.start
