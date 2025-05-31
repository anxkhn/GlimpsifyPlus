import cv2

from ocr_approval.base import OCRApprovalStrategy
from utils.image_utils import ImageUtils


class PHash(OCRApprovalStrategy):
    def permit_ocr(self, new_frame: cv2.Mat, old_frame: cv2.Mat) -> bool:
        if old_frame is None:
            return True
        return not ImageUtils.are_images_similar_phash(new_frame, old_frame)
