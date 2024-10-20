import cv2


class OCRApprovalStrategy:
    def permit_ocr(self, new_frame: cv2.Mat, old_frame: cv2.Mat) -> bool:
        pass
