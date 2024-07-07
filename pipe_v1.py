import os
import random
import string
from yt_down import *
from u1 import *
import shutil
from file_utils import *

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

class YTVideoSummarizer:
    def __init__(self) -> None:
        pass

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
    def run_text_extraction(video_path, tesseract_path, output_path):
        frame_text_data, frames = extract_text_from_video_v3(video_path, tesseract_path, output_path, diff_threshold=0.05, interval=3.0)
        return frame_text_data, frames

    @staticmethod
    def plot_text_vs_frame(frame_text_data, plot_output_path):
        plot_word_count_vs_frame(frame_text_data, plot_output_path)
    
    @staticmethod
    def delete_dir(dir_path):
        # delete only if exists
        if os.path.exists(dir_path): 
            shutil.rmtree(dir_path)

    @staticmethod
    def pipe():
        base_dir = os.path.join(os.getcwd(), "data")
        dir_name = YTVideoSummarizer.get_dir_name()
        
        video_dir = os.path.join(base_dir, dir_name)
        video_name = YTVideoSummarizer.get_video_name(video_dir)
        video_path = os.path.join(video_dir, video_name)
        
        index_path = os.path.join(base_dir, "index.txt")
        with open(index_path, "a") as f:
            f.write(f"{dir_name}_peak_frames: {video_name}\n") 
            
        frames_dir = os.path.join(base_dir, dir_name + "_frames")
        YTVideoSummarizer.delete_dir(frames_dir)
        create_directory(frames_dir)
        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        frame_text_data, frames = YTVideoSummarizer.run_text_extraction(video_path, tesseract_path, frames_dir)
        
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
            # YTVideoSummarizer.delete_dir(plot_path)
        

if __name__ == "__main__":
    # main()
    YTVideoSummarizer.pipe()
    # data/wjndjq
    # random_10_frames("data/vdcakt_frames")