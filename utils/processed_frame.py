import os
from typing import List

from tqdm import tqdm

from ocr_approval.base import OCRApprovalStrategy
from ocr_strategy.ocr_strategy import OCRStrategy
from utils.directory_manager import DirectoryManager
from utils.helper import Helper
from utils.video_processor import VideoProcessor


class ProcessedFrame:
    def __init__(self):
        self.frame_number = 0
        self.char_count = 0

    @staticmethod
    def from_directory(directory, ocr_strategy: OCRStrategy):
        processed_frames = []
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):
                frame = ProcessedFrame()
                frame.frame_number = Helper.get_digits(filename)
                frame.char_count = len(
                    ocr_strategy.extract_clean_text(
                        os.path.join(directory, filename))
                )
                processed_frames.append(frame)
        return processed_frames

    @staticmethod
    def from_video(
        video_path,
        ocr_strategy: OCRStrategy,
        ocr_approval_strategy: OCRApprovalStrategy,
    ):
        processed_frames: List[ProcessedFrame] = []
        old_frame = None

        # Get total frame count for progress tracking
        total_frames = VideoProcessor.get_total_frame_count(video_path, 3)

        # Create progress bar with custom format
        progress_bar = tqdm(
            VideoProcessor.get_frames(video_path, 3),
            total=total_frames,
            desc="Processing Frames",
            bar_format="{desc}: {n}/{total} ({percentage:3.1f}%) | {elapsed} | ETA: {remaining} | {rate_fmt}",
            unit="frames",
        )

        for frame in progress_bar:

            if not ocr_approval_strategy.permit_ocr(frame.frame, old_frame):
                # result should be same as previous frame
                processed_frame = ProcessedFrame()
                processed_frame.frame_number = frame.frame_number

                if processed_frames:
                    processed_frame.char_count = processed_frames[-1].char_count + 1
                else:
                    processed_frame.char_count = 0
                processed_frames.append(processed_frame)
                continue
            old_frame = frame.frame.copy()

            processed_frame = ProcessedFrame()
            processed_frame.frame_number = frame.frame_number
            processed_frame.char_count = ocr_strategy.get_char_count(
                frame.frame)
            processed_frames.append(processed_frame)
        return processed_frames

    @staticmethod
    def from_youtube_video(video_url, directory, ocr_strategy: OCRStrategy):

        Helper.download_youtube_video(video_url, directory)
        video_path = DirectoryManager.get_video_path(directory)
        return ProcessedFrame.from_video(video_path, ocr_strategy)

    @staticmethod
    def get_data_for_plotting(processed_frames: List["ProcessedFrame"]):
        x_data = [frame.frame_number for frame in processed_frames]
        y_data = [frame.char_count for frame in processed_frames]
        return x_data, y_data
