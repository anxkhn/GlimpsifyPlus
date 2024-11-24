from pytubefix import YouTube
from datetime import datetime

def format_time(seconds):
    """Convert seconds to HH:MM:SS format"""
    return str(datetime.fromtimestamp(seconds).strftime('%H:%M:%S'))

def download_video_and_get_chapters(url):
    try:
        # Create YouTube object
        yt = YouTube(url)
        
        # Print video title
        print(f"Video Title: {yt.title}\n")
        
        # Get and print chapters
        if yt.chapters:
            print("Chapter Information:")
            print("-" * 50)
            for i, chapter in enumerate(yt.chapters, 1):
                start_time = format_time(chapter.start_seconds)
                
                # Calculate end time
                if i < len(yt.chapters):
                    end_time = format_time(yt.chapters[i].start_seconds)
                else:
                    end_time = format_time(yt.length)
                
                print(f"Chapter {i}: {chapter.title}")
                print(f"Start Time: {start_time}")
                print(f"End Time: {end_time}")
                print("-" * 50)
        else:
            print("No chapters found in this video")
        
        # Download the video
        print("\nStarting video download...")
        stream = yt.streams.get_highest_resolution()
        stream.download()
        print(f"Video downloaded successfully as: {stream.default_filename}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # URL of the video
    url = "https://www.youtube.com/watch?v=uojIxD6Ofy0"
    
    # Download video and get chapters
    download_video_and_get_chapters(url)