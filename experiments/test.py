import os
import sys


fp = os.path.abspath(__file__)
fp = "/media/vedant/New Volume/DPythonProjects/yt_summarizer/v2"

print(fp)

SCRIPT_DIR = os.path.dirname(fp)

print(SCRIPT_DIR)
sys.path.append(os.path.dirname(SCRIPT_DIR))
 

from v2.helper import Helper

Helper.log("Hello, world!")
