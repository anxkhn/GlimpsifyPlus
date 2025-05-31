from abc import ABC, abstractmethod
from typing import List

from utils.processed_frame import ProcessedFrame


class BaseExtractionStrategy(ABC):

    @abstractmethod
    def extract_frames(self, frames: List[ProcessedFrame]) -> List[ProcessedFrame]:
        pass
