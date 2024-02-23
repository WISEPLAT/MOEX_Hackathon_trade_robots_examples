from abc import ABC, abstractmethod
from typing import Any


class BaseState(ABC):
    @abstractmethod
    def get(self, key: str, default_value: str | None = None) -> str | None:
        """Получение данных из кеша"""

    @abstractmethod
    def set(self, key: str, data: Any) -> None:
        """Установка данных в кеш"""
