from abc import ABC, abstractmethod


class InputStrategy(ABC):
    @abstractmethod
    def proceed(self):
        pass
