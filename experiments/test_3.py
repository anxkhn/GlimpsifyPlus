import sys
fp = "/media/vedant/New Volume/DPythonProjects/yt_summarizer"

sys.path.insert(1, fp)   
fp = "/media/vedant/New Volume/DPythonProjects/yt_summarizer/v2"

sys.path.insert(1, fp)   

from v2.helper import Helper

Helper.log("Hello, world!")
