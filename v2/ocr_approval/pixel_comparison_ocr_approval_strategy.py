from ocr_approval.ocr_approval_strategy import OCRApprovalStrategy
import cv2
from utils.image_utils import ImageUtils


class PixelComparisonOCRApprovalStrategy(OCRApprovalStrategy):
    def permit_ocr(self, new_frame: cv2.Mat, old_frame: cv2.Mat) -> bool:
        if type(old_frame) == type(None):
            return True
        return not ImageUtils.are_images_almost_equal(new_frame, old_frame)