import re
import subprocess
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
    folders = list(dir.iterdir())

    for folder in folders:
        try:
            input = folder.name
            pattern = r"\w{6}_\w{3}_python_object"
            if not re.fullmatch(pattern, input):
                continue
            subprocess.run(
                [
                    "python", "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/main.py",
                    "--input=object",
                    f"--dir={input}", "--ocr=tesseract", "--extraction=prominent_peaks"
                ]
            )
        except:
            print("Exception occurred for: ", folder)


if __name__ == "__main__":
    dir = "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/archives/data_archive_32"
    main(dir)
