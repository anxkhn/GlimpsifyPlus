from ocr_approval.approve_all import ApproveAllApprovalStrategy
from ocr_approval.base import OCRApprovalStrategy
from ocr_approval.phash import PHash
from ocr_approval.pixel_comparison import PixelComparison
from ocr_approval.reject_all import RejectAllApprovalStrategy


class OCRApprovalStrategyFactory:

    @staticmethod
    def create_strategy(input_type: str) -> OCRApprovalStrategy:
        if input_type == "pixel_comparison":
            return PixelComparison()
        if input_type == "approve_all":
            return ApproveAllApprovalStrategy()
        if input_type == "reject_all":
            return RejectAllApprovalStrategy()
        if input_type == "phash":
            return PHash()
        raise ValueError("Invalid OCR approval strategy")
