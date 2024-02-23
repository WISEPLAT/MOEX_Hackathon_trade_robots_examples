from abc import ABC, abstractmethod
from typing import Any, Iterable


class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, raw_data: Iterable[dict[str, Any]]) -> Iterable[type]:
        """Метод трансформации данных"""
