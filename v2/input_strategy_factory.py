from youtube_video_url_input_strategy import YouTubeVideoURLInputStrategy
from input_strategy import InputStrategy
from local_video_input_strategy import LocalVideoInputStrategy
from python_object_input_strategy import PythonObjectInputStrategy
from playlist_input_strategy import PlaylistInputStrategy


class InputStrategyFactory:

    @staticmethod
    def create_input_strategy(
        input_type, ocr_strategy, extraction_strategy
    ) -> InputStrategy:
        if input_type == "youtube":
            video_url = input("Enter YouTube video URL: ")
            return YouTubeVideoURLInputStrategy(
                video_url, ocr_strategy, extraction_strategy
            )
        elif input_type == "local":
            directory = input("Enter directory path: ")
            return LocalVideoInputStrategy(directory, ocr_strategy, extraction_strategy)
        elif input_type == "object":
            directory = input("Enter directory path: ")
            return PythonObjectInputStrategy(
                directory, ocr_strategy, extraction_strategy
            )
        elif input_type == "playlist":
            playlist_url = input("Enter YouTube playlist URL: ")
            return PlaylistInputStrategy(
                playlist_url, ocr_strategy, extraction_strategy
            )
        else:
            raise ValueError("Invalid input type")
