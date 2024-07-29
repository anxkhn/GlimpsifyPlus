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
from torchvision.transforms import Resize

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
            
            # Convert to PIL Image for OCR
            pil_image = torchvision.transforms.ToPILImage()(frame.squeeze().cpu())
            
            # Perform OCR
            text = pytesseract.image_to_string(pil_image)
            
            frame_text_data.append((i, text))
            frames.append(frame.squeeze().cpu())
            
            # Save frame
            torchvision.utils.save_image(frame.squeeze(), f"{output_path}/frame_{i}.png")
        
        return frame_text_data, frames

    def plot_word_count_vs_frame(self, frame_text_data, plot_output_path):
        frame_numbers = [data[0] for data in frame_text_data]
        word_counts = [len(data[1].split()) for data in frame_text_data]

        plt.figure(figsize=(20, 8))
        plt.plot(frame_numbers, word_counts, marker='o')
        plt.title('Number of Words vs Frame Number')
        plt.xlabel('Frame Number')
        plt.ylabel('Number of Words')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(plot_output_path)
        plt.close()

    def save_max_info_frames(self, frame_text_data, output_path, frames, threshold=None):
        if threshold is None:
            threshold = sum(len(data[1].split()) for data in frame_text_data) / len(frame_text_data)

        for i, (frame_number, text) in enumerate(frame_text_data):
            if len(text.split()) > threshold:
                frame = frames[i]
                torchvision.utils.save_image(frame, f"{output_path}/frame_{frame_number}.png")

    def process_video(self, video_path):
        dir_name = self.generate_random_word(6)
        base_dir = os.path.join(os.getcwd(), "data", dir_name)
        self.create_directory(base_dir)

        frames_dir = os.path.join(base_dir, "frames")
        self.create_directory(frames_dir)

        frame_text_data, frames = self.extract_text_from_video(video_path, frames_dir)

        plot_path = os.path.join(base_dir, "plot")
        self.create_directory(plot_path)
        self.plot_word_count_vs_frame(frame_text_data, os.path.join(plot_path, "word_count_vs_frame.png"))

        peak_output_path = os.path.join(base_dir, "peak_frames")
        self.create_directory(peak_output_path)
        self.save_max_info_frames(frame_text_data, peak_output_path, frames)

        return base_dir

if __name__ == "__main__":
    summarizer = GPUVideoSummarizer()
    video_path = input("Enter the path to the video file: ")
    output_dir = summarizer.process_video(video_path)
    print(f"Processing complete. Output saved in {output_dir}")