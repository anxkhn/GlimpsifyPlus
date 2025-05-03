from video2pdf.extraction_strategy.k_transactions_extraction_strategy import KTransactionsExtractionStrategy
from video2pdf.extraction_strategy.key_moments_extraction_strategy import KeyMomentsExtractionStrategy


class ExtractionStrategyFactory:
    @staticmethod
    def create_extraction_strategy(extraction_type):
        if extraction_type == "k_transactions":
            return KTransactionsExtractionStrategy()
        elif extraction_type == "key_moments":
            return KeyMomentsExtractionStrategy()
        else:
            raise ValueError("Invalid extraction type")
