import os
import random
import string
from yt_down import *
from u1 import *
import shutil
from file_utils import *

import io
import sys

# Set the default encoding for sys.stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def generate_random_word(length):
    """Generates a random word of given length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def create_directory(directory_name):
    """Creates a directory with the given name."""
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")

def random_10_frames(dir):
    # Get the list of all files in directory tree at given path
    list_of_files = list()
    for (dirpath, dirnames, filenames) in os.walk(dir):
        list_of_files += [os.path.join(dirpath, file) for file in filenames]

    # Get 10 random files
    random_files = random.sample(list_of_files, 10)
    # return random_files
    new_dir = dir + "_10_" + generate_random_word(3)
    print(f"New directory: {new_dir}")
    create_directory(new_dir)
    # copy to new directory
    for file in random_files:
        shutil.copy(file, new_dir)

def main():
    video_url = input("Enter the URL of the YouTube video (or folder path): ")  # Replace with your desired video URL
    if ":" in video_url:
        # Generate a random 6-digit word
        random_word = generate_random_word(6)
        random_word = "data/" + random_word
        print(f"Random word: {random_word}")

        # Create a directory using the random word as the name
        create_directory(random_word)

        output_directory = os.path.join(os.getcwd(), random_word)  # Change this to your desired output directory
        download_youtube_video(video_url, output_directory)

        # get frames
        output_path = random_word + "_frames"
        # frame_dir = frame_dir_1  
        create_directory(output_path)
        # video_path = "data/v1_t5.mp4"
        # rename the file in the random_word directory to v1.mp4
        os.rename(output_directory + "/" + os.listdir(output_directory)[0], output_directory + "/v1.mp4")
        video_path = output_directory + "/v1.mp4"
    random_word = f"data/{video_url}" 
    output_directory = os.path.join(os.getcwd(), random_word)  # Change this to your desired output directory
    video_path = output_directory + "/v1.mp4"

    # Path to the Tesseract OCR executable
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows
    # tesseract_path = r"/usr/bin/tesseract"  # Linux/macOS

    # Path to save the improved frame
    # output_path = "frames3/frame.jpg" 
    # output_path = frame_dir

    # Extract text with a difference threshold of 0.05 (5%)
    # extract_text_from_video(video_path, tesseract_path, output_path, diff_threshold=0.05, interval=1.0)
    # plot_output_path = random_word + "_plot.png"
    plot_output_dir = os.path.join(os.getcwd(), random_word + "_plot")
    create_directory(plot_output_dir)
    plot_output_path = os.path.join(os.path.join(os.getcwd(), random_word + "_plot"), "word_count_vs_frame.png")
    
    peak_output_path = random_word + "_peak_frames"
    frame_text_data, frames = extract_text_from_video_v3(video_path, tesseract_path, output_path, diff_threshold=0.05, interval=3.0)
    plot_word_count_vs_frame(frame_text_data, plot_output_path)
    save_max_info_frames(frame_text_data, peak_output_path, frames)
    threshhold = input("Enter the threshhold for the peak frames (or n): ")
    if threshhold != "n":
        save_max_info_frames(frame_text_data, peak_output_path + "_" + threshhold, frames, float(threshhold))
    should_clean_up = input("Do you want to clean up the frames directory? (y/n): ")
    if should_clean_up.lower() == "y":
        delete_directories_without_keyword("data", "_peak_frames")
        
    # delete_directories_without_keyword("data", "_peak_frames")
    
    # random_10_frames(output_path)
import pickle
class YTVideoSummarizer:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_frames_from_dir(dir_path):
        list_of_files = list()
        for (dirpath, dirnames, filenames) in os.walk(dir_path):
            list_of_files += [file for file in filenames]
        return list_of_files

    @staticmethod
    def add_text_to_frames_and_save(input_dir, list_of_files, output_dir):
        n = len(list_of_files)
        print(list_of_files)
        for i, file in enumerate(list_of_files):
            frame_path = os.path.join(input_dir, file)
            frame = cv2.imread(frame_path)
            text = f"Glimpsify {i+1}/{n}"
            # frame = cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size, _ = cv2.getTextSize(text, font, 0.51, 1)
            text_x = 10
            text_y = frame.shape[0] - 10
            # cv2.rectangle(frame, (text_x, text_y - text_size[1] - 10), (text_x + text_size[0], text_y), (85, 26, 58), cv2.FILLED)
            # cv2.putText(frame, text, (text_x, text_y - 5), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            

            overlay = frame.copy()
            
            # Draw the filled rectangle on the overlay image
            cv2.rectangle(overlay, (text_x, text_y - text_size[1] - 10), (text_x + text_size[0], text_y), (85, 26, 58), cv2.FILLED)
            cv2.putText(overlay, text, (text_x, text_y - 5), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Blend the overlay with the original image using alpha blending
            opacity = 0.6
            cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)
            
            output_path = os.path.join(output_dir, file)
            cv2.imwrite(output_path, frame)

    @staticmethod
    def generate_random_word(length):
        """Generates a random word of given length."""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))
    
    @staticmethod
    def create_directory(directory_name):
        """Creates a directory with the given name."""
        try:
            os.mkdir(directory_name)
            print(f"Directory '{directory_name}' created successfully.")
        except FileExistsError:
            print(f"Directory '{directory_name}' already exists.")
    @staticmethod
    def get_video_name(output_directory):
        video_name = os.listdir(output_directory)[0]
        return video_name
        
    @staticmethod
    def download_video(video_url):
        random_word = generate_random_word(6) 
        print(f"Random word: {random_word}")
        output_directory = os.path.join(os.getcwd(), "data", random_word)
        create_directory(output_directory)
        download_youtube_video(video_url, output_directory)
        return random_word
    
    @staticmethod
    def get_dir_name():
        video_url = input("Enter the URL of the YouTube video (or folder path): ")
        if ":" in video_url:
            dir_name = YTVideoSummarizer.download_video(video_url)
        else:
            dir_name = video_url
        return dir_name
        
             

    
    @staticmethod
    def run_text_extraction(video_path, tesseract_path, output_path, interval=3.0):
        # frame_text_data, frames = extract_text_from_video_v3(video_path, tesseract_path, output_path, diff_threshold=0.05, interval=3.0)
        frame_text_data, frames = extract_text_from_video_v3(video_path, tesseract_path, output_path, diff_threshold=0.05, interval=interval)
        return frame_text_data, frames

    @staticmethod
    def plot_text_vs_frame(frame_text_data, plot_output_path):
        # plot_word_count_vs_frame(frame_text_data, plot_output_path)
        """
        Plot the number of words versus frame number and save as PNG.

        Args:
            frame_text_data (list): List of tuples containing (frame_number, text).
            output_path (str): Path to save the plot PNG.
        """
        frame_numbers = [data[0] for data in frame_text_data]
        word_counts = [len(data[1].split()) for data in frame_text_data]

        # plt.figure(figsize=(16, 8))
        # larger figure so that all frame numbers are visible on x-axis
        # plt.figure(figsize=(20, 8))
        # find the size of the figure depending on the number of frames and the values of word_counts
        weight_y = 10
        weight_x = 7
        plt.figure(figsize=(len(frame_numbers) / weight_x, max(word_counts) /weight_y))
        plt.plot(frame_numbers, word_counts, marker='o')
        plt.title('Number of Words vs Frame Number')
        plt.xlabel('Frame Number')
        plt.ylabel('Number of Words')

        # Add both vertical and horizontal gridlines
        plt.grid(True, axis='both', linestyle='--', alpha=0.7)

        # Ensure all frame numbers are visible on x-axis
        plt.xticks(frame_numbers, rotation=45, ha='right')

        # Ensure all word counts are visible on y-axis
        min_count = min(word_counts)
        max_count = max(word_counts)
        plt.ylim(max(0, min_count - 1), max_count + 1)
        # plt.yticks(range(max(0, min_count - 1), max_count + 2))    # Set y-ticks to only show values present in the data
        unique_word_counts = sorted(set(word_counts))
        plt.yticks(unique_word_counts)

        # Adjust layout to prevent cutting off axis labels
        plt.tight_layout()

        plt.savefig(plot_output_path, dpi=300)
        plt.close()
    
    @staticmethod
    def delete_dir(dir_path):
        # delete only if exists
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

    @staticmethod
    def pipe():
        base_dir = os.path.join(os.getcwd(), "data")
        dir_name = YTVideoSummarizer.get_dir_name()
        
        video_dir = os.path.join(base_dir, dir_name)
        video_name = YTVideoSummarizer.get_video_name(video_dir)
        video_path = os.path.join(video_dir, video_name)
        
        index_path = os.path.join(base_dir, "index.txt")
        with open(index_path, "a", encoding='utf-8') as f:
            f.write(f"{dir_name}_peak_frames: {video_name}\n") 
            
        frames_dir = os.path.join(base_dir, dir_name + "_frames")
        YTVideoSummarizer.delete_dir(frames_dir)
        create_directory(frames_dir)
        
        
        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        frame_text_data, frames = YTVideoSummarizer.run_text_extraction(video_path, tesseract_path, frames_dir, interval=3)
        
        
        frame_text_data_dir = os.path.join(base_dir, dir_name + "_frame_text_data")
        YTVideoSummarizer.delete_dir(frame_text_data_dir)
        create_directory(frame_text_data_dir)
        
        frame_text_data_file = os.path.join(frame_text_data_dir, "frame_text_data.pkl")
        frames_file = os.path.join(frame_text_data_dir, "frames.pkl")
        YTVideoSummarizer.store_python_objects(frame_text_data, frame_text_data_file)
        YTVideoSummarizer.store_python_objects(frames, frames_file)
        
        plot_path = os.path.join(base_dir, dir_name + "_plot")
        YTVideoSummarizer.delete_dir(plot_path)
        create_directory(plot_path)
        
        YTVideoSummarizer.plot_text_vs_frame(frame_text_data, os.path.join(plot_path, "word_count_vs_frame.png"))
        
        peak_output_path = os.path.join(base_dir, dir_name + "_peak_frames")
        YTVideoSummarizer.delete_dir(peak_output_path)
        create_directory(peak_output_path)
        save_max_info_frames(frame_text_data, peak_output_path, frames)
        
        inp = input("Enter the threshhold for the peak frames (or n): ")
        if inp != "n":
            thresh = float(inp)
            peak_output_path = peak_output_path + "_" + str(thresh)
            YTVideoSummarizer.delete_dir(peak_output_path)
            create_directory(peak_output_path)
            
            save_max_info_frames(frame_text_data, peak_output_path, frames, thresh)
        
        should_clean_up = input("Do you want to clean up the frames directory? (y/n): ")
        
        
        if should_clean_up.lower() == "y":
            YTVideoSummarizer.delete_dir(video_dir)
            YTVideoSummarizer.delete_dir(frames_dir)
            YTVideoSummarizer.delete_dir(plot_path)
            YTVideoSummarizer.delete_dir(frame_text_data_dir) 
            
        

if __name__ == "__main__":
    YTVideoSummarizer.pipe()
    
    # input_dir = "D:\DPythonProjects\yt_summarizer\data\limyws_peak_frames_96.5"
    # lis_of_files = YTVideoSummarizer.get_frames_from_dir(input_dir)
    # output_dir = "D:\DPythonProjects\yt_summarizer\data\limyws_peak_frames_96.5_with_text"
    # YTVideoSummarizer.create_directory(output_dir)
    # YTVideoSummarizer.add_text_to_frames_and_save(input_dir, lis_of_files, output_dir)
    
    
    # data/wjndjq
    # random_10_frames("data/vdcakt_frames")