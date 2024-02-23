from abc import ABC, abstractmethod
from typing import Any


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self) -> dict[str, Any]:
        """Метод извлечения данных"""
