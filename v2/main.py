from input_strategy_factory import InputStrategyFactory
from ocr_strategy_factory import OCRStrategyFactory
from extraction_strategy_factory import ExtractionStrategyFactory
from input_strategy import InputStrategy


def main():
    # ocr_type = input("Enter OCR type: ")
    ocr_type = "tesseract"
    ocr_strategy = OCRStrategyFactory.create_ocr_strategy(ocr_type)

    extraction_type = "k_transactions"
    # extraction_type = "key_moments"
    extraction_strategy = ExtractionStrategyFactory.create_extraction_strategy(
        extraction_type
    )

    # input_type = input("Enter input type: ")
    # input_type = "youtube"
    # input_type = "playlist"
    # input_type = "local"
    input_type = "object"
    input_strategy: InputStrategy = InputStrategyFactory.create_input_strategy(
        input_type, ocr_strategy, extraction_strategy
    )
    input_strategy.proceed()


if __name__ == "__main__":
    main()
