import os
from pathlib import Path

module_dir = os.path.dirname(__file__)
BASE_DIR = Path(module_dir).joinpath("../data").resolve()
BASE_DIR = str(BASE_DIR)
