from input_strategy.base import BaseInputStrategy
from input_strategy.local_file import LocalFileInput
from input_strategy.pickle import PickleInput
from input_strategy.youtube import YouTubeInput


class InputStrategyFactory:

    @staticmethod
    def create_input_strategy(
        input_type,
        ocr_strategy,
        extraction_strategy,
        ocr_approval_strategy,
        url=None,
        directory=None,
    ) -> BaseInputStrategy:
        # The directory path for pickle should be like `xxxxxx_python_object`
        if input_type == "youtube":
            return YouTubeInput(
                url, ocr_strategy, extraction_strategy, ocr_approval_strategy
            )
        if input_type == "local":
            return LocalFileInput(
                directory, ocr_strategy, extraction_strategy, ocr_approval_strategy
            )
        if input_type == "pickle":
            return PickleInput(directory, ocr_strategy, extraction_strategy)
        raise ValueError("Invalid input type")
