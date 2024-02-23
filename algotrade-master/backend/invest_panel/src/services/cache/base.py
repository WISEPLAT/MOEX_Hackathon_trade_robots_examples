from abc import ABC, abstractmethod
from typing import Any


class BaseCache(ABC):
    @abstractmethod
    async def get(self, key: str, default_value: str | None = None) -> str | None:
        """Получение данных из хранилище"""

    @abstractmethod
    async def set(self, key: str, data: Any, expire: int) -> None:
        """Установка данных в хранилище"""

    @abstractmethod
    def delete(self, key: str) -> None:
        """Удаление данных из хранилище"""
