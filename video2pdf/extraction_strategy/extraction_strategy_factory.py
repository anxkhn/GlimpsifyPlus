from video2pdf.extraction_strategy.k_transactions_extraction_strategy import KTransactionsExtractionStrategy
from video2pdf.extraction_strategy.key_moments_extraction_strategy import KeyMomentsExtractionStrategy
from video2pdf.extraction_strategy.timestamp_extraction_strategy import TimestampExtractionStrategy


class ExtractionStrategyFactory:
    @staticmethod
    def create_extraction_strategy(extraction_type):
        if extraction_type == "k_transactions":
            return KTransactionsExtractionStrategy()
        elif extraction_type == "key_moments":
            return KeyMomentsExtractionStrategy()
        elif extraction_type == "timestamps":
            timestamps = eval(input("Enter the timestamps: "))
            return TimestampExtractionStrategy(timestamps)
        else:
            raise ValueError("Invalid extraction type")
