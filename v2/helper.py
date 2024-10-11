import re
import yt_down
from random_generator import RandomGenerator
from directory_manager import DirectoryManager
import os
from pytubefix import Playlist
import cv2
import pickle

from constants import BASE_DIR


class Helper:
    @staticmethod
    def get_digits(text: str) -> int:
        return int(re.sub(r"\D", "", text))

    @staticmethod
    def download_youtube_video(video_url: str, directory: str) -> str:

        yt_down.download_youtube_video(video_url, directory)
        video_file_name = DirectoryManager.get_video_path(directory)
        return os.path.join(directory, video_file_name)

    @staticmethod
    def get_youtube_playlist_urls(playlist_url: str) -> list:
        playlist = Playlist(playlist_url)
        return playlist.video_urls

    @staticmethod
    def save_image(frame_output_path, frame_number, video_path):
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        cv2.imwrite(frame_output_path, frame)
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def save_extracted_frames(extracted_frames, video_path, extracted_frames_directory):
        cap = cv2.VideoCapture(video_path)
        for frame in extracted_frames:
            frame_output_path = os.path.join(
                extracted_frames_directory, f"frame_{frame.frame_number}.jpg"
            )
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame.frame_number)
            ret, frame = cap.read()
            cv2.imwrite(frame_output_path, frame)
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def clean_text(text: str) -> str:
        # Replace multiple whitespaces with a single space

        # Remove punctuation and special characters
        text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        text = text.lower()

        return text

    @staticmethod
    def save_python_objects(python_objects, python_object_path):
        with open(python_object_path, "wb") as f:
            pickle.dump(python_objects, f)

    @staticmethod
    def save_text(text, text_file_path):
        with open(text_file_path, "w") as f:
            f.write(text)

    @staticmethod
    def append_text(text, text_file_path):
        with open(text_file_path, "a") as f:
            f.write(text)

    @staticmethod
    def index_results(directory, video_file_path):
        formatted_text = f"{directory} -> {video_file_path}"
        result_file_path = os.path.join(BASE_DIR, "results.txt")
        Helper.append_text(formatted_text, result_file_path)

    @staticmethod
    def load_python_object(python_object_path):
        with open(python_object_path, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def load_text(text_file_path):
        with open(text_file_path, "r") as f:
            return f.read()


if __name__ == "__main__":
    print(Helper.get_digits("frame_234.jpg"))
