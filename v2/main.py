import argparse
from input_strategy_factory import InputStrategyFactory
from ocr_strategy_factory import OCRStrategyFactory
from extraction_strategy_factory import ExtractionStrategyFactory
from input_strategy import InputStrategy
from ocr_approval.ocr_approval_strategy_factory import OCRApprovalStrategyFactory
from helper import Helper
from directory_manager import DirectoryManager
import os


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process a video and extract key frames."
    )
    parser.add_argument(
        "--input",
        required=True,
        choices=["youtube", "local", "object", "playlist"],
        help="Specify the input type.",
    )
    parser.add_argument(
        "--url", help="Provide YouTube video/playlist URL if applicable."
    )
    parser.add_argument(
        "--start_from",
        type=int,
        help="Specify the start frame number for playlist input.",
    )
    parser.add_argument(
        "--dir", help="Specify the local directory if input type is 'local'."
    )
    parser.add_argument(
        "--ocr_approval",
        choices=["pixel_comparison", "approve_all"],
        default="pixel_comparison",
        help="Specify the OCR approval strategy.",
    )
    parser.add_argument(
        "--ocr",
        choices=["tesseract", "easy"],
        default="easy",
        help="Specify the OCR strategy.",
    )
    parser.add_argument(
        "--extraction",
        choices=["k_transactions", "key_moments"],
        default="k_transactions",
        help="Specify the extraction strategy.",
    )
    parser.add_argument(
        "--k", type=int, help="Specify the number of key frames to extract."
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Cleanup intermediate files after processing.",
    )
    return parser.parse_args()


def cleanup_directory(directory):
    if os.path.exists(directory):
        DirectoryManager.delete_directory(directory)
        print(f"Cleaned up directory: {directory}")


def main():
    args = parse_arguments()
    Helper.setup()

    ocr_approval_strategy = OCRApprovalStrategyFactory.create_strategy(
        args.ocr_approval
    )
    ocr_strategy = OCRStrategyFactory.create_ocr_strategy(args.ocr)
    extraction_strategy = ExtractionStrategyFactory.create_extraction_strategy(
        args.extraction
    )

    if args.k:
        extraction_strategy.k = args.k

    input_strategy: InputStrategy = InputStrategyFactory.create_input_strategy(
        args.input,
        ocr_strategy,
        extraction_strategy,
        ocr_approval_strategy,
        args.url,
        args.dir,
        args.start_from,
    )

    directory = input_strategy.proceed()

    if args.cleanup:
        cleanup_directory(directory)
        cleanup_directory(directory + "_extracted_frames")
        cleanup_directory(directory + "_python_object")
        cleanup_directory(directory + "_plot")


if __name__ == "__main__":
    main()
