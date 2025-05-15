import subprocess
import time

from video2pdf.utils.helper import Helper


def main(urls):
    for url in urls:
        try:
            subprocess.run(
                [
                    "python", "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/main.py",
                    "--input=youtube",
                    f"--url={url}", "--ocr=tesseract", "--extraction=k_transactions", "--k=auto"
                ]
            )
            time.sleep(10)
        except:
            print("Exception occurred for: ", url)


if __name__ == "__main__":
    playlist_url = ""
    # urls = Helper.get_video_urls_from_playlist(playlist_url)
    urls = ["https://www.youtube.com/watch?v=j2-9yymHfeU&list=TLGGEGsAE2D2xJgxNTA1MjAyNQ"]
    main(urls)
