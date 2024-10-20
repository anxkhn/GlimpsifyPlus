from ocr_approval.ocr_approval_strategy import OCRApprovalStrategy
import cv2


class PixelComparisonOCRApprovalStrategy(OCRApprovalStrategy):
    def permit_ocr(self, new_frame: cv2.Mat, old_frame: cv2.Mat) -> bool:
        if type(old_frame) == type(None):
            return True

        # Convert frames to grayscale
        new_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

        # Compute the absolute difference between the two frames
        diff = cv2.absdiff(new_gray, old_gray)

        # Threshold the difference to get a binary image
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Calculate the percentage of different pixels
        non_zero_count = cv2.countNonZero(thresh)
        total_pixels = new_gray.size
        diff_percentage = (non_zero_count / total_pixels) * 100

        # If the difference is less than a certain threshold, consider the frames almost the same
        return diff_percentage > 5
