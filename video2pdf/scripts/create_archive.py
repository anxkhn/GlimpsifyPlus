import re
import shutil
from pathlib import Path


def move_folders(dir: str | Path, archive_number: int) -> None:
    dir = Path(dir)

    to_move = r"\w{6}_\w{3}_.*"
    to_move_2 = r"\w{6}_\w{3}"

    folders_to_move = []

    all_folders = dir.glob("*/")
    for folder in all_folders:
        if re.fullmatch(to_move, folder.name) or re.fullmatch(to_move_2, folder.name):
            folders_to_move.append(folder)

    archive_dir = dir.parent / "archives" / f"data_archive_{archive_number}"
    archive_dir.mkdir()

    for folder in folders_to_move:
        shutil.move(str(folder), str(archive_dir))

    result_src = dir / "results.txt"
    result_src.is_file()

    result_dst = archive_dir / "results.txt"

    shutil.move(str(result_src), str(result_dst))


def move_files(dir: str | Path, archive_number: int) -> None:
    dir = Path(dir)

    to_move = r"\w{6}_\w{3}_.*.pdf"
    to_move_2 = r"\w{6}_\w{3}.pdf"

    files_to_move = []

    all_files = dir.glob("*.pdf")
    for file in all_files:
        if re.fullmatch(to_move, file.name) or re.fullmatch(to_move_2, file.name):
            files_to_move.append(file)

    archive_dir = dir.parent / "archives" / f"data_archive_{archive_number}"
    archive_dir.mkdir()

    for file in files_to_move:
        shutil.move(str(file), str(archive_dir / file.name))


def move_results_file(archive_dir, dir):
    result_src = dir / "results.txt"
    result_src.is_file()
    result_dst = archive_dir / "results.txt"
    shutil.move(str(result_src), str(result_dst))


if __name__ == "__main__":
    archive_number = 26
    dir = r"/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/data"
    move_folders(dir, archive_number)

    archive_number += 1
    move_files(dir, archive_number)
