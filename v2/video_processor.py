import cv2
from typing import Iterator
from frame import Frame


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
                    yield Frame(frame_number, frame)

                frame_number += 1
        finally:
            cap.release()

    
    @staticmethod
    def get_timestamp_from_frame_number(video_path: str, frame_number: int) -> float:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        timestamp = frame_number / fps
        cap.release()
        return timestamp