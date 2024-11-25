from video_processor import VideoProcessor
from directory_manager import DirectoryManager
from helper import Helper

if __name__ == "__main__":
    directory = "data/ikgmbd"
    video_path = DirectoryManager.get_video_path(directory)
    frame_number = 5040
    timestamp = VideoProcessor.get_timestamp_from_frame_number(video_path, frame_number)
    print(timestamp)
