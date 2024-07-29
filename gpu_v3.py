import os
import random
import string
import torch
import torchvision
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract
from torchvision.io import read_video
from torchvision.transforms import Resize, ToPILImage
import shutil
import pickle
from yt_down import download_youtube_video

class GPUVideoSummarizer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        # Set the path to tesseract executable
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    @staticmethod
    def generate_random_word(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def create_directory(directory_name):
        os.makedirs(directory_name, exist_ok=True)
        print(f"Directory '{directory_name}' created successfully.")

    @staticmethod
    def get_video_name(output_directory):
        video_name = os.listdir(output_directory)[0]
        return video_name

    @staticmethod
    def download_video(video_url):
        random_word = GPUVideoSummarizer.generate_random_word(6)
        print(f"Random word: {random_word}")
        output_directory = os.path.join(os.getcwd(), "data", random_word)
        GPUVideoSummarizer.create_directory(output_directory)
        download_youtube_video(video_url, output_directory)
        return random_word

    @staticmethod
    def get_dir_name():
        video_url = input("Enter the URL of the YouTube video (or folder path): ")
        if ":" in video_url:
            dir_name = GPUVideoSummarizer.download_video(video_url)
        else:
            dir_name = video_url
        return dir_name

    def extract_text_from_video(self, video_path, output_path, interval=3.0):
        # Read video
        video, _, _ = read_video(video_path)
        video = video.to(self.device)
        
        fps = 30  # Assuming 30 fps, adjust if known
        frame_interval = int(interval * fps)
        
        frame_text_data = []
        frames = []
        
        for i in range(0, video.shape[0], frame_interval):
            frame = video[i].permute(2, 0, 1)  # Change from (H, W, C) to (C, H, W)
            frame = frame.unsqueeze(0)  # Add batch dimension
            
            # Resize frame for consistent processing
            frame = Resize((720, 1280))(frame)
            
            # Convert to PIL Image for OCR and saving
            pil_image = ToPILImage()(frame.squeeze().cpu())
            
            # Perform OCR
            text = pytesseract.image_to_string(pil_image)
            
            frame_text_data.append((i, text))
            frames.append(frame.squeeze().cpu())
            
            # Save frame as PNG
            pil_image.save(f"{output_path}/frame_{i}.png")
        
        return frame_text_data, frames

    def plot_word_count_vs_frame(self, frame_text_data, plot_output_path):
        frame_numbers = [data[0] for data in frame_text_data]
        word_counts = [len(data[1].split()) for data in frame_text_data]

        weight_y = 10
        weight_x = 7
        plt.figure(figsize=(len(frame_numbers) / weight_x, max(word_counts) / weight_y))
        plt.plot(frame_numbers, word_counts, marker='o')
        plt.title('Number of Words vs Frame Number')
        plt.xlabel('Frame Number')
        plt.ylabel('Number of Words')
        plt.grid(True, axis='both', linestyle='--', alpha=0.7)
        plt.xticks(frame_numbers, rotation=45, ha='right')
        unique_word_counts = sorted(set(word_counts))
        plt.yticks(unique_word_counts)
        plt.tight_layout()
        plt.savefig(plot_output_path, dpi=300)
        plt.close()

    def save_max_info_frames(self, frame_text_data, output_path, frames, threshold=None):
        if threshold is None:
            threshold = sum(len(data[1].split()) for data in frame_text_data) / len(frame_text_data)

        for i, (frame_number, text) in enumerate(frame_text_data):
            if len(text.split()) > threshold:
                frame = frames[i]
                pil_image = ToPILImage()(frame)
                pil_image.save(f"{output_path}/frame_{frame_number}.png")

    @staticmethod
    def delete_dir(dir_path):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def store_python_objects(obj, file_path):
        with open(file_path, "wb") as f:
            pickle.dump(obj, f)

    @staticmethod
    def load_python_objects(file_path):
        with open(file_path, "rb") as f:
            obj = pickle.load(f)
        return obj

    def pipe(self):
        base_dir = os.path.join(os.getcwd(), "data")
        dir_name = self.get_dir_name()
        
        video_dir = os.path.join(base_dir, dir_name)
        video_name = self.get_video_name(video_dir)
        video_path = os.path.join(video_dir, video_name)
        
        index_path = os.path.join(base_dir, "index.txt")
        with open(index_path, "a", encoding='utf-8') as f:
            f.write(f"{dir_name}_peak_frames: {video_name}\n")
            
        frames_dir = os.path.join(base_dir, dir_name + "_frames")
        self.delete_dir(frames_dir)
        self.create_directory(frames_dir)
        
        frame_text_data, frames = self.extract_text_from_video(video_path, frames_dir, interval=3)
        
        frame_text_data_dir = os.path.join(base_dir, dir_name + "_frame_text_data")
        self.delete_dir(frame_text_data_dir)
        self.create_directory(frame_text_data_dir)
        
        frame_text_data_file = os.path.join(frame_text_data_dir, "frame_text_data.pkl")
        frames_file = os.path.join(frame_text_data_dir, "frames.pkl")
        self.store_python_objects(frame_text_data, frame_text_data_file)
        self.store_python_objects(frames, frames_file)
        
        plot_path = os.path.join(base_dir, dir_name + "_plot")
        self.delete_dir(plot_path)
        self.create_directory(plot_path)
        
        self.plot_word_count_vs_frame(frame_text_data, os.path.join(plot_path, "word_count_vs_frame.png"))
        
        peak_output_path = os.path.join(base_dir, dir_name + "_peak_frames")
        self.delete_dir(peak_output_path)
        self.create_directory(peak_output_path)
        self.save_max_info_frames(frame_text_data, peak_output_path, frames)
        
        inp = input("Enter the threshold for the peak frames (or n): ")
        if inp != "n":
            thresh = float(inp)
            peak_output_path = peak_output_path + "_" + str(thresh)
            self.delete_dir(peak_output_path)
            self.create_directory(peak_output_path)
            
            self.save_max_info_frames(frame_text_data, peak_output_path, frames, thresh)
        
        should_clean_up = input("Do you want to clean up the frames directory? (y/n): ")
        
        if should_clean_up.lower() == "y":
            self.delete_dir(video_dir)
            self.delete_dir(frames_dir)
            self.delete_dir(plot_path)
            self.delete_dir(frame_text_data_dir)

if __name__ == "__main__":
    summarizer = GPUVideoSummarizer()
    summarizer.pipe()