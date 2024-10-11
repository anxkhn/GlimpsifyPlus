from k_transactions_extraction_strategy import KTransactionsExtractionStrategy


class ExtractionStrategyFactory:
    @staticmethod
    def create_extraction_strategy(extraction_type):
        if extraction_type == "k_transactions":
            return KTransactionsExtractionStrategy()
        else:
            raise ValueError("Invalid extraction type")
