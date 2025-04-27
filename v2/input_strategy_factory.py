from youtube_video_url_input_strategy import YouTubeVideoURLInputStrategy
from input_strategy import InputStrategy
from local_video_input_strategy import LocalVideoInputStrategy
from python_object_input_strategy import PythonObjectInputStrategy
from playlist_input_strategy import PlaylistInputStrategy
import sys

class InputStrategyFactory:

    @staticmethod
    def create_input_strategy(
        input_type, ocr_strategy, extraction_strategy, ocr_approval_strategy, url=None, directory=None, start_from=None
    ) -> InputStrategy:
        if input_type == "youtube":
            return YouTubeVideoURLInputStrategy(
                url, ocr_strategy, extraction_strategy, ocr_approval_strategy
            )
        elif input_type == "local":
            return LocalVideoInputStrategy(
                directory, ocr_strategy, extraction_strategy, ocr_approval_strategy
            )
        elif input_type == "object":
            """The directory path should be like this `xxxxxx_python_object`"""
            return PythonObjectInputStrategy(
                directory, ocr_strategy, extraction_strategy
            )
        elif input_type == "playlist": 
            return PlaylistInputStrategy(
                url,
                start_from,
                ocr_strategy,
                extraction_strategy,
                ocr_approval_strategy,
            )
        else:
            raise ValueError("Invalid input type")
