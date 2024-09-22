import os
import random
import string
import shutil
import logging
import pickle
from abc import ABC, abstractmethod
from typing import List, Tuple

import cv2
import matplotlib.pyplot as plt

from yt_down import download_youtube_video
from u1 import save_max_info_frames
from text_utils import clean_text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VideoDownloader(ABC):
    @abstractmethod
    def download(self, url: str, output_dir: str) -> str:
        pass

class YouTubeDownloader(VideoDownloader):
    def download(self, url: str, output_dir: str) -> str:
        logger.info(f"Downloading YouTube video from {url}")
        return download_youtube_video(url, output_dir)

class OCR(ABC):
    @abstractmethod
    def extract_text(self, img_fp: str) -> str:
        pass

    def extract_clean_text(self, img_fp: str) -> str:
        text = self.extract_text(img_fp)
        return clean_text(text)

class Tesseract(OCR):
    def extract_text(self, img_fp: str) -> str:
        import pytesseract
        from PIL import Image
        return pytesseract.image_to_string(Image.open(img_fp))

class EasyOCR(OCR):
    def __init__(self):
        import easyocr
        self.reader = easyocr.Reader(['en'])

    def extract_text(self, img_fp: str) -> str:
        results = self.reader.readtext(img_fp)
        text = [result[1] for result in results]
        return " ".join(text)

class OCRFactory:
    @staticmethod
    def create_ocr(ocr_type: str) -> OCR:
        if ocr_type == "tesseract":
            return Tesseract()
        elif ocr_type == "easyocr":
            return EasyOCR()
        else:
            raise ValueError("Invalid OCR type")

class VideoProcessor:
    def __init__(self, ocr: OCR, interval: float = 3.0):
        self.ocr = ocr
        self.interval = interval

    def process(self, video_path: str, output_dir: str) -> Tuple[List[Tuple[int, str]], List[cv2.Mat]]:
        logger.info(f"Processing video {video_path} with {self.ocr.__class__.__name__}")
        return self._extract_text_from_video(video_path, output_dir)

    def _extract_text_from_video(self, video_path: str, output_dir: str) -> Tuple[List[Tuple[int, str]], List[cv2.Mat]]:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * self.interval)

        frame_text_data = []
        frames = []
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                frame_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
                cv2.imwrite(frame_path, frame)
                text = self.ocr.extract_clean_text(frame_path)
                frame_text_data.append((frame_count, text))
                frames.append(frame)

            frame_count += 1

        cap.release()
        return frame_text_data, frames

class DataPlotter:
    @staticmethod
    def plot_word_count_vs_frame(frame_text_data: List[Tuple[int, str]], output_path: str):
        logger.info(f"Plotting word count vs frame to {output_path}")
        frame_numbers = [data[0] for data in frame_text_data]
        word_counts = [len(data[1].split()) for data in frame_text_data]

        weight_y, weight_x = 10, 7
        plt.figure(figsize=(len(frame_numbers) / weight_x, max(word_counts) / weight_y))
        plt.plot(frame_numbers, word_counts, marker='o')
        plt.title('Number of Words vs Frame Number')
        plt.xlabel('Frame Number')
        plt.ylabel('Number of Words')
        plt.grid(True, axis='both', linestyle='--', alpha=0.7)
        plt.xticks(frame_numbers, rotation=45, ha='right')
        
        min_count, max_count = min(word_counts), max(word_counts)
        plt.ylim(max(0, min_count - 1), max_count + 1)
        unique_word_counts = sorted(set(word_counts))
        plt.yticks(unique_word_counts)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

class DataPersistence:
    @staticmethod
    def store_object(obj: object, file_path: str):
        logger.info(f"Storing object to {file_path}")
        with open(file_path, "wb") as f:
            pickle.dump(obj, f)

    @staticmethod
    def load_object(file_path: str) -> object:
        logger.info(f"Loading object from {file_path}")
        with open(file_path, "rb") as f:
            return pickle.load(f)

class DirectoryManager:
    @staticmethod
    def create_directory(directory_name: str):
        try:
            os.mkdir(directory_name)
            logger.info(f"Directory '{directory_name}' created successfully.")
        except FileExistsError:
            logger.warning(f"Directory '{directory_name}' already exists.")

    @staticmethod
    def delete_directory(dir_path: str):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            logger.info(f"Directory '{dir_path}' deleted successfully.")

    @staticmethod
    def generate_random_word(length: int) -> str:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

class VideoSummarizerFactory:
    @staticmethod
    def create_downloader(type: str) -> VideoDownloader:
        if type == "youtube":
            return YouTubeDownloader()
        else:
            raise ValueError(f"Unsupported downloader type: {type}")

    @staticmethod
    def create_processor(ocr_type: str, **kwargs) -> VideoProcessor:
        ocr = OCRFactory.create_ocr(ocr_type)
        return VideoProcessor(ocr, **kwargs)

import numpy as np
import pandas as pd
import re

class DataFrameLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_array(self):
        array = np.load(self.filepath, allow_pickle=True)
        array = np.array(array)
        return array

    def create_dataframe(self, array):
        df = pd.DataFrame(array)
        df.rename(columns={0: "frame_id", 1: "text"}, inplace=True)
        self.add_cleaned_text_column(df)
        self.add_char_count_column(df)
        return df

    def clean_text(self, text):
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        text = " ".join(text.split())
        text = text.lower()
        return text

    def char_count(self, text):
        return len(text)

    def add_char_count_column(self, df):
        df["char_count"] = df["cleaned_text"].apply(self.char_count)
        return df

    def add_cleaned_text_column(self, df):
        df["cleaned_text"] = df["text"].apply(self.clean_text)
        return df

def maxProfit(prices, n, k):
    if n <= 1 or k == 0:
        return 0, []

    profit = [[0 for _ in range(k + 1)] for _ in range(n)]
    transactions = [[[] for _ in range(k + 1)] for _ in range(n)]

    for i in range(1, n):
        for j in range(1, k + 1):
            max_so_far = 0
            best_transaction = []

            for l in range(i):
                current_profit = prices[i] - prices[l] + profit[l][j - 1]
                if current_profit > max_so_far:
                    max_so_far = current_profit
                    best_transaction = transactions[l][j - 1] + [(l, i)]

            if max_so_far > profit[i - 1][j]:
                profit[i][j] = max_so_far
                transactions[i][j] = best_transaction
            else:
                profit[i][j] = profit[i - 1][j]
                transactions[i][j] = transactions[i - 1][j]

    return profit[n - 1][k], transactions[n - 1][k]

class YTVideoSummarizer:
    def __init__(self, downloader: VideoDownloader, processor: VideoProcessor):
        self.downloader = downloader
        self.processor = processor

    def summarize(self, video_url: str, base_dir: str):
        dir_name = self._setup_directories(video_url, base_dir)
        video_path = self._download_video(video_url, os.path.join(base_dir, dir_name))
        self._process_video(video_path, base_dir, dir_name)
        self._cleanup(base_dir, dir_name)

    def _setup_directories(self, video_url: str, base_dir: str) -> str:
        if ":" in video_url:
            dir_name = DirectoryManager.generate_random_word(6)
        else:
            dir_name = video_url
        
        DirectoryManager.create_directory(os.path.join(base_dir, dir_name))
        return dir_name

    def _download_video(self, video_url: str, output_dir: str) -> str:
        if ":" in video_url:
            self.downloader.download(video_url, output_dir)
        return os.path.join(output_dir, os.listdir(output_dir)[0])

    def _process_video(self, video_path: str, base_dir: str, dir_name: str):
        frames_dir = os.path.join(base_dir, f"{dir_name}_frames")
        DirectoryManager.create_directory(frames_dir)

        frame_text_data, frames = self.processor.process(video_path, frames_dir)

        self._save_data(base_dir, dir_name, frame_text_data, frames)
        self._plot_data(base_dir, dir_name, frame_text_data)
        self._save_peak_frames(base_dir, dir_name, frame_text_data, frames)

        # New addition: Calculate and save profit frames
        self._calculate_and_save_profit_frames(base_dir, dir_name, frame_text_data, frames)


    def _save_data(self, base_dir: str, dir_name: str, frame_text_data: List[Tuple[int, str]], frames: List[cv2.Mat]):
        data_dir = os.path.join(base_dir, f"{dir_name}_frame_text_data")
        DirectoryManager.create_directory(data_dir)

        DataPersistence.store_object(frame_text_data, os.path.join(data_dir, "frame_text_data.pkl"))
        DataPersistence.store_object(frames, os.path.join(data_dir, "frames.pkl"))

    def _plot_data(self, base_dir: str, dir_name: str, frame_text_data: List[Tuple[int, str]]):
        plot_dir = os.path.join(base_dir, f"{dir_name}_plot")
        DirectoryManager.create_directory(plot_dir)

        DataPlotter.plot_word_count_vs_frame(frame_text_data, os.path.join(plot_dir, "word_count_vs_frame.png"))


    def _calculate_and_save_profit_frames(self, base_dir: str, dir_name: str, frame_text_data: List[Tuple[int, str]], frames: List[cv2.Mat]):
        # Create DataFrame
        df = pd.DataFrame(frame_text_data, columns=['frame_id', 'text'])
        df['char_count'] = df['text'].apply(len)

        # Get input for k
        k = int(input("Enter the number of transactions (k): "))

        # Calculate max profit
        prices = df['char_count'].values
        n = len(prices)
        max_profit, transactions = maxProfit(prices, n, k)

        logger.info(f"Maximum profit: {max_profit}")
        logger.info(f"Transactions: {transactions}")

        # Save profit frames
        profit_frames_dir = os.path.join(base_dir, f"{dir_name}_profits")
        DirectoryManager.create_directory(profit_frames_dir)

        for _, sell in transactions:
            frame_index = df.iloc[sell]['frame_id']  # Get the actual frame_id
            frame = frames[sell]
            frame_path = os.path.join(profit_frames_dir, f"profit_frame_{frame_index}.jpg")
            cv2.imwrite(frame_path, frame)

        logger.info(f"Profit frames saved in {profit_frames_dir}") 

    def _save_peak_frames(self, base_dir: str, dir_name: str, frame_text_data: List[Tuple[int, str]], frames: List[cv2.Mat]):
        peak_output_path = os.path.join(base_dir, f"{dir_name}_peak_frames")
        DirectoryManager.create_directory(peak_output_path)
        save_max_info_frames(frame_text_data, peak_output_path, frames)

        threshold = input("Enter the threshold for the peak frames (or n): ")
        if threshold != "n":
            threshold = float(threshold)
            peak_output_path = f"{peak_output_path}_{threshold}"
            DirectoryManager.create_directory(peak_output_path)
            save_max_info_frames(frame_text_data, peak_output_path, frames, threshold)

    def _cleanup(self, base_dir: str, dir_name: str):
        should_clean_up = input("Do you want to clean up the frames directory? (y/n): ")
        if should_clean_up.lower() == "y":
            DirectoryManager.delete_directory(os.path.join(base_dir, dir_name))
            DirectoryManager.delete_directory(os.path.join(base_dir, f"{dir_name}_frames"))
            DirectoryManager.delete_directory(os.path.join(base_dir, f"{dir_name}_plot"))
            DirectoryManager.delete_directory(os.path.join(base_dir, f"{dir_name}_frame_text_data"))

def main():
    base_dir = os.path.join(os.getcwd(), "data")
    video_url = input("Enter the URL of the YouTube video (or folder path): ")
    # ocr_type = input("Enter the OCR type (tesseract/easyocr): ")
    ocr_type = "tesseract" 

    factory = VideoSummarizerFactory()
    downloader = factory.create_downloader("youtube")
    processor = factory.create_processor(ocr_type, interval=3.0)

    summarizer = YTVideoSummarizer(downloader, processor)
    summarizer.summarize(video_url, base_dir)

if __name__ == "__main__":
    main()