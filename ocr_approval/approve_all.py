import cv2

from ocr_approval.base import OCRApprovalStrategy


class ApproveAllApprovalStrategy(OCRApprovalStrategy):
    def permit_ocr(self, new_frame: cv2.Mat, old_frame: cv2.Mat) -> bool:
        return True
