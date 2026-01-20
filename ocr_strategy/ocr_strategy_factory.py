from ocr_strategy.easy_ocr import EasyOCR
from ocr_strategy.tesseract_ocr import Tesseract


class OCRStrategyFactory:
    @staticmethod
    def create_ocr_strategy(ocr_type):
        if ocr_type == "tesseract":
            return Tesseract()
        if ocr_type == "easy":
            return EasyOCR()
        raise ValueError("Invalid OCR type")
