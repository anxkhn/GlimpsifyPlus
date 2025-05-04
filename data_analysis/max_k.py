# %%
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

# %%
import matplotlib.pyplot as plt

# %%
dir_name = "acjrso"
base_dir = "D:\DPythonProjects\yt_summarizer\data"

# %%
# frames_pkl = r"D:\DPythonProjects\yt_summarizer\data_archive_1\ixfwsm_frame_text_data\frames.pkl"
# frame_text_data_pkl = (
#     r"D:\DPythonProjects\yt_summarizer\data_archive_1\ixfwsm_frame_text_data\frame_text_data.pkl"
# )

frames_pkl = f"{base_dir}\\{dir_name}_frame_text_data\\frames.pkl"
frame_text_data_pkl = f"{base_dir}\\{dir_name}_frame_text_data\\frame_text_data.pkl"
frames_pkl, frame_text_data_pkl

# %%
import re

# %%

import pandas as pd
import numpy as np


class DataFrameLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_array(self):
        # Load the NumPy array from the file path
        array = np.load(self.filepath, allow_pickle=True)
        # I want numpy array
        array = np.array(array)
        return array

    def create_dataframe(self, array):
        # Create a DataFrame from the NumPy array
        df = pd.DataFrame(array)
        df.rename(columns={0: "frame_id", 1: "text"}, inplace=True)
        self.add_cleaned_text_column(df)
        self.add_char_count_column(df)
        return df

    def print_dataframe(self, df):
        # Print the DataFrame
        print(df)

    # df["cleaned_text"] = df["text"].apply(clean_text)
    # df["char_count"] = df["cleaned_text"].apply(char_count)

    def clean_text(self, text):
        # Remove special characters and numbers
        text = re.sub(r"[^a-zA-Z\s]", "", text)

        # Remove extra whitespace
        text = " ".join(text.split())

        # Convert to lowercase
        text = text.lower()

        return text

    def char_count(self, text):
        # Count the number of characters in the text
        char_count = len(text)
        return char_count

    def add_char_count_column(self, df):
        # Add a new column to the DataFrame
        df["char_count"] = df["cleaned_text"].apply(self.char_count)
        return df

    def add_cleaned_text_column(self, df):
        # Add a new column to the DataFrame
        df["cleaned_text"] = df["text"].apply(self.clean_text)
        return df
    
    def get_k_max_profit(self, df, k):
        # Get the maximum profit and transactions
        prices = df["char_count"].values
        n = len(prices)
        profit, transactions = maxProfit(prices, n, k)
        return profit, transactions

# %%
# Create an instance of the DataFrameLoader class
loader = DataFrameLoader(frame_text_data_pkl)

# Load the array
array = loader.load_array()
type(array)

# %%
print(array.shape)
array[:5]

# %%
# Create the DataFrame
df = loader.create_dataframe(array)

# Print the DataFrame
loader.print_dataframe(df)

# %%
frames_loader = DataFrameLoader(frames_pkl)
frames_array = frames_loader.load_array()
print(frames_array.shape)

# %%
df.shape

# %%
ns_chars = df.char_count
ns_chars.describe()

Q1 = ns_chars.quantile(0.25)
Q3 = ns_chars.quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

ns_chars = ns_chars[(ns_chars >= lower_bound) & (ns_chars <= upper_bound)]
ns_chars.describe()

# %%
df.shape

# %%
class DataVisualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

        weight_y = 10
        weight_x = 7
        max_chars = df["char_count"].max() / 4

        # plt.figure(figsize=( df.shape[0]  / weight_x, max_chars /weight_y))
        self.figsize = (df.shape[0] / weight_x, max_chars / weight_y)

    @staticmethod
    def plot_decorator(func):
        def wrapper(*args, **kwargs):
            # set style to normal style
            plt.style.use("classic")
            plt.figure(figsize=args[0].figsize)
            func(*args, **kwargs)
            # plt.grid(True, axis="both", linestyle="--", alpha=0.7)
            # color should be light of the grid
            plt.grid(True, axis="both", linestyle="--", alpha=0.7, color="lightgrey")
            plt.xticks(args[0].df["frame_id"], rotation=45, ha="right")

            plt.show()

        return wrapper

    @plot_decorator
    def plot_char_count(self):
        # Plot a histogram of the character count
        plt.hist(self.df["char_count"], bins=30, color="skyblue", edgecolor="black")
        plt.title("Character Count in Text")
        plt.xlabel("Character Count")
        plt.ylabel("Frequency")

    @plot_decorator
    def plot_frame_id_vs_char_count(self):
        # Plot the frame_id vs char_count
        plt.scatter(self.df["frame_id"], self.df["char_count"], color="skyblue")
        plt.title("Frame ID vs Character Count")
        plt.xlabel("Frame ID")
        plt.ylabel("Character Count")

    @plot_decorator
    def plot_frame_id_vs_char_count_line(self):
        # Plot the frame_id vs char_count with a line connecting the points
        plt.plot(self.df["frame_id"], self.df["char_count"], color="blue")
        plt.title("Frame ID vs Character Count")
        plt.xlabel("Frame ID")
        plt.ylabel("Character Count")

    @plot_decorator
    def plot_moving_averages(self):
        df = self.df
        plt.plot(
            df["frame_id"], df["char_count"], color="skyblue", label="Character Count"
        )
        plt.plot(
            df["frame_id"],
            df["SMA_short"],
            color="orange",
            label="Short Moving Average",
        )
        plt.plot(
            df["frame_id"], df["SMA_long"], color="red", label="Long Moving Average"
        )
        plt.title("Moving Averages")
        plt.xlabel("Frame ID")
        plt.ylabel("Character Count")
        plt.legend()

    @plot_decorator
    def plot_crossover_points(self, crossover_points):
        df = self.df
        self.plot_moving_averages()
        plt.scatter(
            crossover_points["frame_id"],
            crossover_points["char_count"],
            color="black",
            label="Crossover Points",
        )
        plt.title("Crossover Points")
        plt.xlabel("Frame ID")
        plt.ylabel("Character Count")
        plt.legend()

# %%
normal = df.iloc[ns_chars.index]
normal.head()
normal.shape

# %%
from typing import *

# %%
normal_data_loader = DataFrameLoader("")


# %%
p, trans  = normal_data_loader.get_k_max_profit(normal, 10)
trans

# make a new array of second values of trans
scatter_x = [x[1] for x in trans]
scatter_y = [normal.iloc[x[1]]["char_count"] for x in trans]
scatter_x, scatter_y


# %%
normal["frame_id"]

# %%

# Plot the trans points and normal dataframe char_count on the same graph
plt.plot(normal["frame_id"], normal["char_count"], color="skyblue", label="Normal Data") 

plt.scatter(scatter_x, scatter_y, color="red", label="Profit Points")

# at the point of scatter_x, scatter_y also write the text scatter_x
for i, txt in enumerate(scatter_x):
    plt.annotate(txt, (scatter_x[i], scatter_y[i]))
 
plt.title("Trans Points and Normal Char Count")
plt.xlabel("Frame ID")
plt.ylabel("Character Count")
plt.legend()
plt.show()

# %%
dv_normal = DataVisualizer(normal)
dv_normal.plot_frame_id_vs_char_count_line()

# %%
# 227-353 get this inclusive slice and make new df
df_slice = df.iloc[:]
df_slice.head()

# %%
dv_slice = DataVisualizer(df_slice)
dv_slice.plot_frame_id_vs_char_count_line()

# %%
k = 3
prices = df_slice["char_count"].values
n = len(prices)

offset = 227

max_profit, transactions = maxProfit(prices, n, k)
print(f"Maximum profit is: {max_profit}")
print("Transactions:")
for buy, sell in transactions:
    print(f"Buy on frame {buy + offset}, sell on frame {sell + offset}")

# %%
dv = DataVisualizer(df)

# %%
dv.plot_frame_id_vs_char_count_line()

# %%
# dv.plot_char_count()

# %%
# dv.plot_frame_id_vs_char_count()

# %%
class Analyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calculate_moving_averages(self, short_window=20, long_window=50):
        self.df["SMA_short"] = self.df["char_count"].rolling(window=short_window).mean()
        self.df["SMA_long"] = self.df["char_count"].rolling(window=long_window).mean()
        self.df["crossover"] = np.where(
            self.df["SMA_short"] > self.df["SMA_long"], 1, 0
        )
        self.df["crossover_change"] = self.df["crossover"].diff()
        return df

    def crossover_points(self):
        # Find the crossover points
        crossover_points = self.df[self.df["crossover_change"] != 0]
        return crossover_points


analyser = Analyzer(df)
df_with_ma = analyser.calculate_moving_averages()

crossover_points = analyser.crossover_points()

# %%
crossover_points.head()

# %%
dv2 = DataVisualizer(df_with_ma)

# %%
dv2.plot_crossover_points(crossover_points)

# %%
dv2.plot_frame_id_vs_char_count_line()

# %%



