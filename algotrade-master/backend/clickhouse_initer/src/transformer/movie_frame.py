from typing import Iterable, Any

from transformer.base import BaseTransformer
from models.movie import MovieFrameDatagram, EventType, MovieRating


class MovieFrameTransformer(BaseTransformer):
    def transform(
        self, raw_data: Iterable[dict[str, Any]]
    ) -> Iterable[MovieFrameDatagram]:
        for data in raw_data:
            movie_rating = MovieRating(rating=data.get("rating"))

            yield MovieFrameDatagram(
                user_id=data.get("user_id"),
                movie_id=data.get("movie_id"),
                movie_duration=movie_rating.duration,
                frame_time=movie_rating.start,
                event_type=EventType.STARTING,
            )

            yield MovieFrameDatagram(
                user_id=data.get("user_id"),
                movie_id=data.get("movie_id"),
                movie_duration=movie_rating.duration,
                frame_time=movie_rating.stop,
                event_type=EventType.STOPPED,
            )
