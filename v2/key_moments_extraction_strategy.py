from extraction_strategy import ExtractionStrategy
from helper import Helper
from processed_frame import ProcessedFrame
from typing import List

class KeyMomentsExtractionStrategy(ExtractionStrategy):
    def __init__(self):
        self.video_url = None
        self.frame_rate = None

    def extract_frames(self, frames: List[ProcessedFrame]) -> List[ProcessedFrame]:
        key_moments = Helper.get_key_moments(self.video_url)
        key_frame_numbers = Helper.get_key_moments_from_seconds(key_moments, self.frame_rate)

        
        key_frames = []
        i = 0
        j = 0

        n = len(frames)
        m = len(key_frame_numbers)

        while j < m:
            while frames[i].frame_number < key_frame_numbers[j] and i < n:
                i += 1
            
            if frames[i].frame_number < key_frame_numbers[j]:
                key_frames.append(frames[i])
            
            j += 1
        
        return key_frames

            


