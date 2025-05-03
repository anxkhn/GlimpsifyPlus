import matplotlib.pyplot as plt
from typing import List
from processed_frame import ProcessedFrame


class DataPlotter:
    @staticmethod
    def plot_data(
        x_data,
        y_data,
        x_label,
        y_label,
        title,
        output_path,
        x_ticks=None,
        y_ticks=None,
        extracted_frames: List[ProcessedFrame] = None,
    ):
        weight_y, weight_x = 10, 7
        num = None
        if y_data:
            num = max(y_data)
        else:
            num = weight_y * 10
        h = num / weight_y
        plt.figure(figsize=(max(20, len(x_data) / weight_x), h))
        plt.plot(x_data, y_data, marker="o")
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True, axis="both", linestyle="--", alpha=0.7)
        plt.xticks(x_data, rotation=45, ha="right")

        min_y, max_y = min(y_data), max(y_data)
        plt.ylim(max(0, min_y - 1), max_y + 1)
        unique_y_data = sorted(set(y_data))
        plt.yticks(unique_y_data)

        if x_ticks:
            plt.xticks(x_ticks)
        if y_ticks:
            plt.yticks(y_ticks)

        if extracted_frames:
            for frame in extracted_frames:
                plt.annotate(
                    f"Extracted Frame ({frame.frame_number})",
                    (frame.frame_number, frame.char_count),
                    xytext=(5, 5),
                    textcoords="offset points",
                    color="green",
                    fontweight="bold",
                )
                plt.plot(
                    frame.frame_number,
                    frame.char_count,
                    "o",
                    color="green",
                    markersize=10,
                )

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()
