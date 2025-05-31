from typing import List

from extraction_strategy.base_extraction_strategy import BaseExtractionStrategy
from utils.helper import Helper
from utils.processed_frame import ProcessedFrame


class TimestampExtractionStrategy(BaseExtractionStrategy):
    def __init__(self, timestamps: List):
        self.timestamps = timestamps
        self.frame_rate = None

    def extract_frames(self, frames: List[ProcessedFrame]) -> List[ProcessedFrame]:
        key_moments = self.timestamps
        key_frame_numbers = Helper.get_key_frame_numbers(
            key_moments, self.frame_rate)
        key_frames = []

        for frame_number in key_frame_numbers:
            processed_frame = ProcessedFrame()
            processed_frame.frame_number = frame_number
            key_frames.append(processed_frame)

        return key_frames
