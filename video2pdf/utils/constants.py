import os
from pathlib import Path

module_dir = os.path.dirname(__file__)
BASE_DIR = Path(module_dir).joinpath("../archives/data_archive_32").resolve()
BASE_DIR = str(BASE_DIR)
