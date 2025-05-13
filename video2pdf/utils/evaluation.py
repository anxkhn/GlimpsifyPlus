from pathlib import Path
from typing import List

import pandas as pd


def clean_df(pdf_files_df: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicate rows"""
    return pdf_files_df.drop_duplicates(subset=["internal_id"], keep="last")


def build_pdf_files_df(files: List[Path]):
    """Build PDF files dataframe having columns `internal_id` and `pdf_path`"""
    pdfs_files_df = pd.DataFrame(columns=["internal_id", "pdf_path"])
    for file in files:
        new_row = {"internal_id": file.stem.split("_")[0], "pdf_path": str(file)}
        pdfs_files_df = pd.concat([pdfs_files_df, pd.DataFrame([new_row])])
    return pdfs_files_df


def get_pdf_files(folder_path: str | Path):
    """Get PDF files in the folder"""
    folder_path = Path(folder_path)
    return folder_path.glob("*.pdf")
