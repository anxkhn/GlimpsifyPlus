import subprocess
import time
from pathlib import Path


def main(dir):
    dir = Path(dir)

    for folder in dir.iterdir():
        try:
            input = folder.name
            if len(input) != 6:
                continue
            subprocess.run(
                [
                    "python", "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/main.py",
                    "--input=local",
                    f"--dir={input}", "--ocr=tesseract", "--k=auto"
                ]
            )
            time.sleep(10)
        except:
            print("Exception occurred for: ", folder)


if __name__ == "__main__":
    dir = "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/data"
    main(dir)
