from typing import Iterator

import cv2

from utils.frame import Frame


class VideoProcessor:

    @staticmethod
    def get_frames(video_path: str, interval: int) -> Iterator[Frame]:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval)

        try:
            frame_number = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_number % frame_interval == 0:
                    # Create a copy of the frame to ensure the original buffer can be released
                    frame_copy = frame.copy()
                    yield Frame(frame_number, frame_copy)
                    # Explicitly delete the copy after yielding if not needed
                    del frame

                frame_number += 1
        finally:
            cap.release()
            # Call garbage collector explicitly to help clean up any remaining references
            import gc

            gc.collect()

    @staticmethod
    def get_timestamp_from_frame_number(video_path: str, frame_number: int) -> float:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        timestamp = frame_number / fps
        cap.release()
        return timestamp

    @staticmethod
    def get_formatted_time(seconds: int) -> str:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"
