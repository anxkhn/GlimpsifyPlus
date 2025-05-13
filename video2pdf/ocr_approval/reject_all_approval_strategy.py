import cv2

from video2pdf.ocr_approval.ocr_approval_strategy import OCRApprovalStrategy


class RejectAllApprovalStrategy(OCRApprovalStrategy):
    def permit_ocr(self, new_frame: cv2.Mat, old_frame: cv2.Mat) -> bool:
        return False
