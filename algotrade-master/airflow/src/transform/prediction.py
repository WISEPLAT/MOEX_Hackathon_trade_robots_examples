from typing import Any, Iterator

from src.transform.base import BaseTransformer
from src.models.prediction import PredictionModel


class PredictionTransformer(BaseTransformer):
    def transform(self, data: Iterator[Any], to_dict: bool = False) -> Iterator[Any]:

        for elem in data:
            elem = PredictionModel(
                secid=elem.get('secid'),
                algorithm=elem.get('algorithm'),
                value=elem.get('value'),
                timestamp=elem.get('timestamp')
            )
            yield elem.model_dump() if to_dict else elem
