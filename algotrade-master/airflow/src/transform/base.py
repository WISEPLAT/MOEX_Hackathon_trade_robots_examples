from abc import ABC, abstractmethod
from typing import Iterator, Any


class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, to_dict: bool = False, **kwargs) -> Iterator[Any]:
        """Метод трансформации данных"""
