from ocr_approval.ocr_approval_strategy import OCRApprovalStrategy
import cv2


class ApproveAllApprovalStrategy(OCRApprovalStrategy):
    def permit_ocr(self, new_frame: cv2.Mat, old_frame: cv2.Mat) -> bool:
        return True
