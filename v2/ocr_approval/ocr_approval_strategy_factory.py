from ocr_approval.pixel_comparison_ocr_approval_strategy import (
    PixelComparisonOCRApprovalStrategy,
)
from ocr_approval.ocr_approval_strategy import OCRApprovalStrategy
from ocr_approval.approve_all_approval_strategy import ApproveAllApprovalStrategy

class OCRApprovalStrategyFactory:

    @staticmethod
    def create_strategy(input_type: str) -> OCRApprovalStrategy:
        if input_type == "pixel_comparison":
            return PixelComparisonOCRApprovalStrategy()
        elif input_type == "approve_all":
            return ApproveAllApprovalStrategy()
        else:
            raise ValueError("Invalid OCR approval strategy")
