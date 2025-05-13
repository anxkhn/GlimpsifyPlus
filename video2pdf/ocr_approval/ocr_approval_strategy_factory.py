from video2pdf.ocr_approval.approve_all_approval_strategy import ApproveAllApprovalStrategy
from video2pdf.ocr_approval.ocr_approval_strategy import OCRApprovalStrategy
from video2pdf.ocr_approval.pixel_comparison_ocr_approval_strategy import (
    PixelComparisonOCRApprovalStrategy,
)
from video2pdf.ocr_approval.reject_all_approval_strategy import RejectAllApprovalStrategy


class OCRApprovalStrategyFactory:

    @staticmethod
    def create_strategy(input_type: str) -> OCRApprovalStrategy:
        if input_type == "pixel_comparison":
            return PixelComparisonOCRApprovalStrategy()
        elif input_type == "approve_all":
            return ApproveAllApprovalStrategy()
        elif input_type == "reject_all":
            return RejectAllApprovalStrategy()
        else:
            raise ValueError("Invalid OCR approval strategy")
