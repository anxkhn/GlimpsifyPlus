import os

from video2pdf.extraction_strategy.extraction_strategy import ExtractionStrategy
from video2pdf.input_strategy.input_strategy import InputStrategy
from video2pdf.ocr_strategy.ocr_strategy import OCRStrategy
from video2pdf.utils.constants import BASE_DIR
from video2pdf.utils.data_plotter import DataPlotter
from video2pdf.utils.directory_manager import DirectoryManager
from video2pdf.utils.helper import Helper
from video2pdf.utils.post_processor import PostProcessor
from video2pdf.utils.processed_frame import ProcessedFrame
from video2pdf.utils.random_generator import RandomGenerator


class PythonObjectInputStrategy(InputStrategy):
    def __init__(
            self,
            directory: str,
            ocr_strategy: OCRStrategy,
            extraction_strategy: ExtractionStrategy,
    ):
        self.directory = os.path.join(BASE_DIR, directory)
        self.ocr_strategy = ocr_strategy
        self.extraction_strategy = extraction_strategy

    def proceed(self):
        new_directory = RandomGenerator.generate_random_word(6)
        new_directory = os.path.join(BASE_DIR, new_directory)
        DirectoryManager.create_directory(new_directory)

        video_path_file_path = os.path.join(self.directory, "video_path.txt")
        video_path = Helper.load_text(video_path_file_path)

        Helper.index_results(new_directory, video_path)

        python_object_path = os.path.join(self.directory, "processed_frames.pkl")
        processed_frames = Helper.load_python_object(python_object_path)

        Helper.log(f"Loaded {len(processed_frames)} frames")

        x_data, y_data = ProcessedFrame.get_data_for_plotting(processed_frames)

        plot_directory = new_directory + "_plot"
        DirectoryManager.create_directory(plot_directory)
        plot_output_path = os.path.join(plot_directory, "plot.png")

        DataPlotter.plot_data(
            x_data,
            y_data,
            "Frame Number",
            "Number of Characters",
            "Number of Characters in OCR Text",
            plot_output_path,
        )

        Helper.log(f"Plotted data to {plot_output_path}")

        extracted_frames = self.extraction_strategy.extract_frames(processed_frames)

        DataPlotter.plot_data(
            x_data,
            y_data,
            "Frame Number",
            "Number of Characters",
            "Number of Characters in OCR Text",
            plot_output_path,
            extracted_frames=extracted_frames,
        )

        extracted_frames_directory = new_directory + "_extracted_frames"
        DirectoryManager.create_directory(extracted_frames_directory)

        Helper.save_extracted_frames(
            extracted_frames, video_path, extracted_frames_directory
        )

        Helper.log(f"Extracted frames to {extracted_frames_directory}")

        list_of_files = os.listdir(extracted_frames_directory)

        PostProcessor.add_text_to_frames_and_save(
            extracted_frames_directory, list_of_files, extracted_frames_directory
        )

        output_pdf_path = new_directory + ".pdf"
        PostProcessor.convert_images_to_pdf(
            extracted_frames_directory, list_of_files, output_pdf_path
        )

        Helper.save_log(video_path, output_pdf_path)
