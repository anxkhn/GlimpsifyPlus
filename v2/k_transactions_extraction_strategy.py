from extraction_strategy import ExtractionStrategy
import pandas as pd
from processed_frame import ProcessedFrame


class KTransactionsExtractionStrategy(ExtractionStrategy):
    def __init__(self):
        self.k = None

    @staticmethod
    def maxProfit(prices, n, k):
        if n <= 1 or k == 0:
            return 0, []

        profit = [[0 for _ in range(k + 1)] for _ in range(n)]
        transactions = [[[] for _ in range(k + 1)] for _ in range(n)]

        for i in range(1, n):
            for j in range(1, k + 1):
                max_so_far = 0
                best_transaction = []

                for l in range(i):
                    current_profit = prices[i] - prices[l] + profit[l][j - 1]
                    if current_profit > max_so_far:
                        max_so_far = current_profit
                        best_transaction = transactions[l][j - 1] + [(l, i)]

                if max_so_far > profit[i - 1][j]:
                    profit[i][j] = max_so_far
                    transactions[i][j] = best_transaction
                else:
                    profit[i][j] = profit[i - 1][j]
                    transactions[i][j] = transactions[i - 1][j]

        return profit[n - 1][k], transactions[n - 1][k]

    def extract_frames(self, frames):
        if self.k is None:
            k = input("Enter the number of transactions (k): ")
            self.k = int(k)
        data = [(frame.frame_number, frame.ocr_text) for frame in frames]
        df = pd.DataFrame(data, columns=["frame_id", "text"])
        df["char_count"] = df["text"].apply(len)

        prices = df["char_count"].values
        n = len(prices)
        max_profit, transactions = self.maxProfit(prices, n, self.k)

        return [frames[sell] for _, sell in transactions]
