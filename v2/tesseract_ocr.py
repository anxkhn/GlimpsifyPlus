from ocr_strategy import OCRStrategy
import pytesseract
from PIL import Image
import cv2
import numpy as np

class Tesseract(OCRStrategy):
    def extract_text(self, img): 
        if isinstance(img, str):
            return pytesseract.image_to_string(Image.open(img))
        elif isinstance(img, np.ndarray):
            return pytesseract.image_to_string(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))