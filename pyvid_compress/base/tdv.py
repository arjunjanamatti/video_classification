from __future__ import annotations
from abc import abstractmethod
from abc import ABC, abstractmethod
import cloudpickle


class Tdv(ABC):

    @abstractmethod
    def persist(self, file_path):
        pass

    @staticmethod
    def load(file_path) -> Tdv:
        with open(file_path, 'rb') as f:
            return cloudpickle.load(f)
