from abc import ABC, abstractmethod


class BaseInputStrategy(ABC):
    @abstractmethod
    def proceed(self):
        pass
