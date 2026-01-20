import argparse
import logging
import os
import platform
import subprocess
import sys

from extraction_strategy.extraction_strategy_factory import ExtractionStrategyFactory
from input_strategy.base import BaseInputStrategy
from input_strategy.factory import InputStrategyFactory
from ocr_approval.factory import OCRApprovalStrategyFactory
from ocr_strategy.ocr_strategy_factory import OCRStrategyFactory
from utils.directory_manager import DirectoryManager
from utils.helper import Helper

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="logs/process.log",
)


def open_file_cross_platform(file_path):
    """Open a file using the default system application."""
    try:
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", file_path])
        elif system == "Windows":
            os.startfile(file_path)
        elif system == "Linux":
            subprocess.run(["xdg-open", file_path])
        else:
            print(
                f"Cannot auto-open file on {system}. Please open manually: {file_path}"
            )
            return False
        return True
    except Exception as e:
        print(f"Failed to open file: {e}")
        return False


def get_user_input(prompt, valid_responses=None):
    """Get user input with validation."""
    while True:
        response = input(prompt).strip().lower()
        if valid_responses is None or response in valid_responses:
            return response
        print(f"Please enter one of: {', '.join(valid_responses)}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Glimpsify: Extract key frames from educational videos and convert to PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract frames from YouTube video (auto-detect count)
  python main.py --input youtube --url "https://www.youtube.com/watch?v=VIDEO_ID"
  
  # Extract specific number of frames
  python main.py --input youtube --url "YOUR_URL" --k 10
  
  # Process local video file
  python main.py --input local --dir "/path/to/video.mp4"
  
  # Process with cleanup (remove intermediate files)
  python main.py --input youtube --url "YOUR_URL" --cleanup
  
  # Generate analysis results file
  python main.py --input youtube --url "YOUR_URL" --create-results

Frame Count Options:
  --k auto    : Automatically detect optimal number of frames (default)
  --k 5       : Extract exactly 5 key frames
  --k 20      : Extract exactly 20 key frames
        """,
    )

    # Required arguments
    parser.add_argument(
        "--input",
        required=True,
        choices=["youtube", "local", "pickle", "playlist"],
        help="Input source type:\n"
        "  youtube   - Single YouTube video\n"
        "  local     - Local video file\n"
        "  playlist  - YouTube playlist\n"
        "  pickle    - Previously saved data",
    )

    # Input source arguments
    parser.add_argument(
        "--url", help="YouTube video/playlist URL (required for youtube/playlist input)"
    )
    parser.add_argument(
        "--dir", help="Local directory or video file path (required for local input)"
    )

    # Processing options
    parser.add_argument(
        "--k",
        type=str,
        default="auto",
        help="Number of key frames to extract:\n"
        "  auto      - Automatically detect optimal count (default)\n"
        "  NUMBER    - Extract specific number of frames (e.g., 5, 10, 20)",
    )

    parser.add_argument(
        "--extraction",
        choices=["k_transactions", "key_moments", "timestamps", "prominent_peaks"],
        default="prominent_peaks",
        help="Frame extraction algorithm:\n"
        "  prominent_peaks - Find frames with most information (default)\n"
        "  k_transactions  - Transaction-based extraction\n"
        "  key_moments     - Use YouTube chapters/moments\n"
        "  timestamps      - Extract at specific times",
    )

    parser.add_argument(
        "--timestamps",
        type=lambda x: list(map(float, map(str.strip, x.split(",")))),
        help="Specific timestamps to extract (comma-separated seconds, e.g., '10.5,30,45.2')",
        default=None,
    )

    # OCR options
    parser.add_argument(
        "--ocr",
        choices=["tesseract", "easy"],
        default="tesseract",
        help="OCR (text recognition) engine:\n"
        "  tesseract - Fast and reliable (default)\n"
        "  easy      - More accurate for complex text",
    )

    parser.add_argument(
        "--ocr_approval",
        choices=["pixel_comparison", "approve_all", "reject_all", "phash"],
        default="phash",
        help="Duplicate frame detection method:\n"
        "  phash           - Perceptual hashing (default, recommended)\n"
        "  pixel_comparison - Exact pixel comparison\n"
        "  approve_all     - Keep all frames\n"
        "  reject_all      - Remove all duplicates",
    )

    # Output options
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Remove intermediate processing files after completion",
    )

    parser.add_argument(
        "--create-results",
        action="store_true",
        help="Generate detailed results.xlsx file with processing statistics",
    )

    # Batch processing
    parser.add_argument(
        "--start_from",
        type=int,
        help="For playlists: skip first N videos (useful for resuming)",
        default=0,
    )

    return parser.parse_args()


def cleanup_directory(directory):
    """Remove a directory if it exists."""
    if os.path.exists(directory):
        DirectoryManager.delete_directory(directory)
        print(f"Cleaned up: {os.path.basename(directory)}")


def main():
    args = parse_arguments()
    Helper.setup()

    print("Glimpsify: Extracting key frames from your video...")
    print("=" * 60)

    # Validate arguments
    if args.input in ["youtube", "playlist"] and not args.url:
        print("Error: --url is required for YouTube input")
        return 1

    if args.input == "local" and not args.dir:
        print("Error: --dir is required for local input")
        return 1

    # Setup strategies
    ocr_approval_strategy = OCRApprovalStrategyFactory.create_strategy(
        args.ocr_approval
    )
    ocr_strategy = OCRStrategyFactory.create_ocr_strategy(args.ocr)
    extraction_strategy = ExtractionStrategyFactory.create_extraction_strategy(
        args.extraction, timestamps=args.timestamps
    )

    # Configure frame count
    if args.k == "auto":
        extraction_strategy.auto_calculate_k = True
        print("Using automatic frame count detection")
    else:
        try:
            k_value = int(args.k)
            extraction_strategy.k = k_value
            print(f"Extracting {k_value} key frames")
        except ValueError:
            print(f"Error: Invalid --k value '{args.k}'. Use 'auto' or a number.")
            return 1

    if args.timestamps:
        extraction_strategy.timestamps = args.timestamps
        print(f"Using specific timestamps: {args.timestamps}")

    # Show configuration
    print(f"OCR Engine: {args.ocr}")
    print(f"Extraction Strategy: {args.extraction}")
    print(f"Duplicate Detection: {args.ocr_approval}")
    print("-" * 60)

    # Process video
    input_strategy: BaseInputStrategy = InputStrategyFactory.create_input_strategy(
        args.input,
        ocr_strategy,
        extraction_strategy,
        ocr_approval_strategy,
        args.url,
        args.dir,
    )

    directory = input_strategy.process()

    print("-" * 60)
    print("Frame extraction complete!")

    # Find generated files
    pdf_path = f"{directory}.pdf"
    is_playlist = args.input == "playlist"

    if os.path.exists(pdf_path):
        print(f"PDF generated: {os.path.basename(pdf_path)}")

        # Ask about video retention (only for single videos, not playlists)
        if not is_playlist and os.path.exists(directory):
            print("\nVideo Storage:")
            keep_video = get_user_input(
                "Would you like to keep the downloaded video for later use? (y/n): ",
                ["y", "yes", "n", "no"],
            )

            if keep_video in ["n", "no"]:
                cleanup_directory(directory)
                print("Video deleted to save disk space")
            else:
                print(f"Video kept in: {directory}")

        # Open PDF or folder
        print(f"\nProcessing complete!")

        if is_playlist:
            data_dir = os.path.dirname(pdf_path)
            print(f"Opening results folder...")
            if open_file_cross_platform(data_dir):
                print(f"Opened folder: {data_dir}")
        else:
            print(f"Opening PDF...")
            if open_file_cross_platform(pdf_path):
                print(f"Opened PDF: {os.path.basename(pdf_path)}")
    else:
        print("Error: PDF was not generated")
        return 1

    # Handle cleanup of intermediate files
    if args.cleanup:
        print(f"\nCleaning up intermediate files...")
        cleanup_directory(directory + "_extracted_frames")
        cleanup_directory(directory + "_python_object")
        cleanup_directory(directory + "_plot")
        print("Cleanup complete")

    # Optionally remove results file
    if not args.create_results:
        results_file = "data/results.xlsx"
        if os.path.exists(results_file):
            os.remove(results_file)
    else:
        results_file = "data/results.xlsx"
        if os.path.exists(results_file):
            print(f"Analysis results saved: {results_file}")

    print(f"\nSummary:")
    print(f"   PDF: {os.path.basename(pdf_path)}")
    if not is_playlist and os.path.exists(directory):
        print(f"   Video: {os.path.basename(directory)}")
    if args.create_results and os.path.exists("data/results.xlsx"):
        print(f"   Results: results.xlsx")

    return 0


if __name__ == "__main__":
    sys.exit(main())
