from input_strategy import InputStrategy
from ocr_strategy import OCRStrategy
from extraction_strategy import ExtractionStrategy
from random_generator import RandomGenerator
from directory_manager import DirectoryManager
import os
from helper import Helper
from constants import BASE_DIR
from youtube_video_url_input_strategy import YouTubeVideoURLInputStrategy
from k_transactions_extraction_strategy import KTransactionsExtractionStrategy
from ocr_approval.ocr_approval_strategy import OCRApprovalStrategy


class PlaylistInputStrategy(InputStrategy):
    def __init__(
        self,
        playlist_url: str,
        start_from: int,
        ocr_strategy: OCRStrategy,
        extraction_strategy: ExtractionStrategy,
        ocr_approval_strategy: OCRApprovalStrategy,
    ):
        self.playlist_url = playlist_url

        "The video number to start processing from. Skip the previous videos."
        self.start_from = start_from
        self.ocr_strategy = ocr_strategy
        self.extraction_strategy = extraction_strategy
        self.ocr_approval_strategy = ocr_approval_strategy

    def proceed(self):
        directory = RandomGenerator.generate_random_word(6)
        directory = os.path.join(BASE_DIR, directory)
        DirectoryManager.create_directory(directory)

        video_urls = Helper.get_video_urls_from_playlist(self.playlist_url)
        counter = 0
        for video_url in video_urls:
            try:
                print("\n\n\n=====================================")
                print(f"#{self.start_from + counter} Processing video: {video_url}")
                print("=====================================")
                counter += 1
                if counter < self.start_from:
                    continue

                # TODO: Ideally, this should not be here. Check if there is a better way to do this.
                if isinstance(
                    self.extraction_strategy, KTransactionsExtractionStrategy
                ):
                    # TODO: This is a hack. Fix this.
                    # video_duration = Helper.get_video_duration(video_url)
                    # number_of_slides = Helper.get_number_of_slides(video_duration)
                    # self.extraction_strategy.k = number_of_slides
                    self.extraction_strategy.auto_calculate_k = True
                    self.extraction_strategy.k = None

                video_input_strategy = YouTubeVideoURLInputStrategy(
                    video_url,
                    self.ocr_strategy,
                    self.extraction_strategy,
                    self.ocr_approval_strategy,
                )

                video_input_strategy.proceed()
            except Exception as e:
                print("Error processing video:", video_url)
                print("Counter:", counter)
                with open("error_log.txt", "a") as error_log:
                    error_log.write(f"Error processing video: {video_url}\n")
                    error_log.write(f"Error: {str(e)}\n")
                    error_log.write(f"Counter: {counter}\n")
                    error_log.write("=====================================\n")
                continue
