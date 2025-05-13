import cv2

from video2pdf.ocr_approval.ocr_approval_strategy import OCRApprovalStrategy
from video2pdf.utils.image_utils import ImageUtils

# TODO: Add another OCRApprovalStrategy based on percentual_hash
class PixelComparisonOCRApprovalStrategy(OCRApprovalStrategy):
    def permit_ocr(self, new_frame: cv2.Mat, old_frame: cv2.Mat) -> bool:
        if type(old_frame) == type(None):
            return True
        return not ImageUtils.are_images_almost_equal(new_frame, old_frame)
