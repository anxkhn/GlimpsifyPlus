import cv2
import pytesseract
import os
import difflib
import numpy as np
from typing import Generator, Tuple

def set_tesseract_path(tesseract_path: str) -> None:
    """
    Set the path to the Tesseract OCR executable.

    Args:
        tesseract_path (str): The path to the Tesseract OCR executable.
    """
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

def read_frames(video_path: str, interval: float = 0.0) -> Generator[Tuple[cv2.Mat, int], None, None]:
    """
    Read frames from the video file.

    Args:
        video_path (str): The path to the video file.
        interval (float, optional): The interval (in seconds) between frames. Defaults to 0.0 (read all frames).

    Yields:
        Tuple[cv2.Mat, int]: The next frame from the video and its frame number.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    skip_frames = int(fps * interval)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % skip_frames == 0:
            yield frame, frame_count // skip_frames

        frame_count += 1

    cap.release()

def process_frame(frame: cv2.Mat) -> str:
    """
    Process a frame and extract text using OCR.

    Args:
        frame (cv2.Mat): The frame to process.

    Returns:
        str: The extracted text from the frame.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, config=r"--psm 6")
    return text

def calculate_text_difference(text1: str, text2: str) -> float:
    """
    Calculate the difference between two texts using sequence matcher.

    Args:
        text1 (str): The first text.
        text2 (str): The second text.

    Returns:
        float: The ratio of similarity between the texts (0.0 - 1.0).
    """
    matcher = difflib.SequenceMatcher(None, text1, text2)
    return matcher.ratio()


def calculate_frame_difference(frame1: cv2.Mat, frame2: cv2.Mat, threshold: float = 0.1) -> bool:
    """
    Calculate the difference between two frames using point processing.

    Args:
        frame1 (cv2.Mat): The first frame.
        frame2 (cv2.Mat): The second frame.
        threshold (float, optional): The threshold for the difference ratio. Defaults to 0.1.

    Returns:
        bool: True if the difference ratio is greater than the threshold, False otherwise.
    """
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    diff_ratio = np.sum(diff > 0) / (diff.shape[0] * diff.shape[1])
    return diff_ratio > threshold

def save_frame(frame: cv2.Mat, output_path: str, frame_number: int) -> None:
    """
    Save a frame to the specified output path with a frame number.

    Args:
        frame (cv2.Mat): The frame to save.
        output_path (str): The path to save the frame.
        frame_number (int): The frame number to burn on the frame.
    """
 
    output_path = os.path.join(output_path, f"frame_{frame_number}.jpg" )
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f"Frame: {frame_number}"
    text_size, _ = cv2.getTextSize(text, font, 1, 2)
    text_x = 10
    text_y = frame.shape[0] - 10
    cv2.rectangle(frame, (text_x, text_y - text_size[1] - 10), (text_x + text_size[0], text_y), (0, 0, 0), cv2.FILLED)
    cv2.putText(frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imwrite(output_path, frame)

def extract_text_from_video(video_path: str, tesseract_path: str, output_path: str, interval: float = 0.0, diff_threshold: float = 0.1) -> None:
    """
    Extract text from each frame of a video using OCR and save improved frames.

    Args:
        video_path (str): The path to the video file.
        tesseract_path (str): The path to the Tesseract OCR executable.
        output_path (str): The path to save the improved frame.
        interval (float, optional): The interval (in seconds) between frames. Defaults to 0.0 (read all frames).
        diff_threshold (float, optional): The threshold for the difference ratio between frames. Defaults to 0.1.
    """
    set_tesseract_path(tesseract_path)
    previous_text = ""
    previous_frame = None
    frame_number = 0

    for frame, frame_idx in read_frames(video_path, interval):
        if previous_frame is not None and not calculate_frame_difference(frame, previous_frame, diff_threshold):
            continue

        text = process_frame(frame)
        text_difference = calculate_text_difference(text, previous_text)

        if text_difference < 0.9:  # Adjust the threshold as needed
            if previous_frame is not None:
                save_frame(previous_frame, output_path, frame_number)
                frame_number += 1
            previous_text = text
            previous_frame = frame.copy()

    # Save the last frame if it wasn't saved
    if previous_frame is not None:
        save_frame(previous_frame, output_path, frame_number)


import matplotlib.pyplot as plt


def plot_word_count_vs_frame(frame_text_data: list, output_path: str) -> None:
    """
    Plot the number of words versus frame number and save as PNG.

    Args:
        frame_text_data (list): List of tuples containing (frame_number, text).
        output_path (str): Path to save the plot PNG.
    """
    frame_numbers = [data[0] for data in frame_text_data]
    word_counts = [len(data[1].split()) for data in frame_text_data]

    plt.figure(figsize=(16, 8))
    plt.plot(frame_numbers, word_counts, marker='o')
    plt.title('Number of Words vs Frame Number')
    plt.xlabel('Frame Number')
    plt.ylabel('Number of Words')
    
    # Add vertical gridlines
    plt.grid(True, axis='both', linestyle='--', alpha=0.7)
    
    # Ensure all frame numbers are visible on x-axis
    plt.xticks(frame_numbers, rotation=45, ha='right')
    
    # Adjust layout to prevent cutting off x-axis labels
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300)
    plt.close()

def extract_text_from_video_v2(video_path: str, tesseract_path: str, output_path: str, interval: float = 0.0, diff_threshold: float = 0.1) -> None:
    set_tesseract_path(tesseract_path)
    previous_text = ""
    previous_frame = None
    frame_number = 0
    frame_text_data = []

    for frame, frame_idx in read_frames(video_path, interval):
        if previous_frame is not None and not calculate_frame_difference(frame, previous_frame, diff_threshold):
            continue

        text = process_frame(frame)
        text_difference = calculate_text_difference(text, previous_text)

        if text_difference < 0.9:  # Adjust the threshold as needed
            if previous_frame is not None:
                save_frame(previous_frame, output_path, frame_number)
                frame_text_data.append((frame_number, previous_text))
                frame_number += 1
            previous_text = text
            previous_frame = frame.copy()

    # Save the last frame if it wasn't saved
    if previous_frame is not None:
        save_frame(previous_frame, output_path, frame_number)
        frame_text_data.append((frame_number, previous_text))

    # Plot word count vs frame number
    plot_output_path = os.path.join(os.path.dirname(output_path), "word_count_vs_frame.png")
    plot_word_count_vs_frame(frame_text_data, plot_output_path)
    
    
import numpy as np

def find_peaks(arr):
    arr = np.array(arr)
    peaks = np.zeros(len(arr), dtype=bool)
    
    if arr[0] > arr[1]:
        peaks[0] = True
    if arr[-1] > arr[-2]:
        peaks[-1] = True
    
    for i in range(1, len(arr) - 1):
        if arr[i] > arr[i-1] and arr[i] > arr[i+1]:
            peaks[i] = True
    
    return peaks

def extract_text_from_video_v3(video_path: str, tesseract_path: str, output_path: str, interval: float = 0.0, diff_threshold: float = 0.1) -> None:
    set_tesseract_path(tesseract_path)
    previous_text = ""
    previous_frame = None
    frame_number = 0
    frame_text_data = []
    frames = []

    for frame, frame_idx in read_frames(video_path, interval):
        if previous_frame is not None and not calculate_frame_difference(frame, previous_frame, diff_threshold):
            continue

        text = process_frame(frame)
        text_difference = calculate_text_difference(text, previous_text)

        if text_difference < 0.9:  # Adjust the threshold as needed
            if previous_frame is not None:
                save_frame(previous_frame, output_path, frame_number)
                frame_text_data.append((frame_number, previous_text))
                frames.append(previous_frame)
                frame_number += 1
            previous_text = text
            previous_frame = frame.copy()

    # Save the last frame if it wasn't saved
    if previous_frame is not None:
        save_frame(previous_frame, output_path, frame_number)
        frame_text_data.append((frame_number, previous_text))
        frames.append(previous_frame)

    # Plot word count vs frame number
    plot_output_path = os.path.join(os.path.dirname(output_path), "word_count_vs_frame.png")
    peak_output_path = os.path.join(os.path.dirname(output_path), "peak_frames") 
    

    
    
    return frame_text_data, frames

def save_max_info_frames(frame_text_data, peak_output_path, frames, threshold = 0):
# Find and save local maxima frames
    frame_numbers, texts = zip(*frame_text_data)
    word_counts = [len(text.split()) for text in texts]
    peaks = find_peaks(word_counts)

    os.makedirs(peak_output_path, exist_ok=True)
    for i, is_peak in enumerate(peaks):
        if is_peak and word_counts[i] > threshold:
            peak_frame_path = os.path.join(peak_output_path, f"peak_frame_{frame_numbers[i]}.jpg")
            cv2.imwrite(peak_frame_path, frames[i])

    print(f"Saved {sum(peaks)} peak frames to {peak_output_path}")

    
if __name__ == "__main__":
    # Path to the video file
    video_path = "data/ajyowi/v1.mp4"

    # Path to the Tesseract OCR executable
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows
    # tesseract_path = r"/usr/bin/tesseract"  # Linux/macOS

    # Path to save the improved frame
    output_path = "data/frames3/frame.jpg" 

    # Extract text with a difference threshold of 0.05 (5%)
    extract_text_from_video_v3(video_path, tesseract_path, output_path, diff_threshold=0.05, interval=3.0)