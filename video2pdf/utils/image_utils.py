import cv2
import numpy as np


class ImageUtils:

    @staticmethod
    def are_images_almost_equal(image1: np.ndarray, image2: np.ndarray) -> bool:
        # Convert frames to grayscale
        image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # Compute the absolute difference between the two frames
        diff = cv2.absdiff(image1_gray, image2_gray)

        # Threshold the difference to get a binary image
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Calculate the percentage of different pixels
        non_zero_count = cv2.countNonZero(thresh)
        total_pixels = image1_gray.size
        diff_percentage = (non_zero_count / total_pixels) * 100

        # If the difference is less than a certain threshold, consider the frames almost the same
        return diff_percentage < 0.5
