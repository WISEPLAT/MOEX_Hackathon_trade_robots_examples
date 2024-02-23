from abc import ABC, abstractmethod
from typing import Any, Iterator


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self) -> Iterator[Any]:
        """Метод извлечения данных"""
