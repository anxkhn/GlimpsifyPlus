import subprocess
import time
from pathlib import Path

reference_pdfs_folder_path = Path(r"/home/vedant/Downloads/reference-pdfs-v1")
from video2pdf.utils.evaluation import get_pdf_files, build_pdf_files_df, clean_df

# ---- Get pdf files from folder
reference_pdf_files = get_pdf_files(reference_pdfs_folder_path)

# ---- Build df for the pdf files
# ---- Columns would be `internal_id`, `pdf_path`
reference_pdf_files_df = build_pdf_files_df(reference_pdf_files)

# ---- Clean df; drop duplicate pdfs for same internal_id
reference_pdf_files_df = clean_df(reference_pdf_files_df)


def main(dir):
    dir = Path(dir)

    for folder in dir.iterdir():
        if reference_pdf_files_df[reference_pdf_files_df["internal_id"] == folder.name].empty:
            print(f"Skipping {folder}")
            continue

        try:
            input = folder.name
            if len(input) != 6:
                continue
            subprocess.run(
                [
                    "python", "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/main.py",
                    "--input=local",
                    f"--dir={input}", "--ocr=tesseract", "--extraction=k_transactions", "--k=auto"
                ]
            )
            time.sleep(10)
        except:
            print("Exception occurred for: ", folder)


if __name__ == "__main__":
    dir = "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/data"
    main(dir)
