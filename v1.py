from pytube import YouTube

# Specify the URL of the YouTube video
url = "https://www.youtube.com/watch?v=q_zyuPOd3PQ"  # Replace with your desired video URL

# Create a YouTube object
yt = YouTube(url)
yt.headers.update({'User-Agent': 'Mozilla/5.0'})

# Get the highest resolution stream
video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

# Check if a stream is available
if video is not None:
    print(f"Downloading video: {yt.title}")
    video.download()
    print("Download completed!")
else:
    print("No MP4 stream found.")