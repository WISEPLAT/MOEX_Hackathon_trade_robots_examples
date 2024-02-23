from abc import ABC, abstractmethod
from typing import Iterator


class BaseLoader(ABC):
    @abstractmethod
    def load(self, data: Iterator[type]):
        raise NotImplementedError
