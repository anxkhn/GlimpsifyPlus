import os
from typing import Optional
from pytube import YouTube

def download_youtube_video(url: str, output_dir: str = ".") -> None:
    """
    Download a YouTube video in MP4 format.

    Args:
        url (str): The URL of the YouTube video.
        output_dir (str, optional): The directory to save the downloaded video. Defaults to the current directory.
    """
    yt = YouTube(url)
    video = get_highest_resolution_mp4_stream(yt)

    if video:
        print(f"Downloading video: {yt.title}")
        try:
            video.download(output_dir)
            print("Download completed successfully!")
        except Exception as e:
            print(f"Error occurred during download: {e}")
    else:
        print("No MP4 stream found.")

def get_highest_resolution_mp4_stream(yt: YouTube) -> Optional[pytube.Stream]:
    """
    Get the highest resolution MP4 stream for the given YouTube object.

    Args:
        yt (YouTube): The YouTube object.

    Returns:
        Optional[pytube.Stream]: The highest resolution MP4 stream, or None if not found.
    """
    return yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=q_zyuPOd3PQ"  # Replace with your desired video URL
    output_directory = os.path.join(os.getcwd(), "downloads")  # Change this to your desired output directory

    download_youtube_video(video_url, output_directory)