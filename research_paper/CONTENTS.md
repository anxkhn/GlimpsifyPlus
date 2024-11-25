## Flow of the project "Key Frame Extraction from Educational Videos"

User enters youtube video link
The video is downloaded
Video is ingested frame by frame
New frame is compared with the previous frame using the following algorithm
```
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
```
If the frames are almost the same, the frame is skipped
If the frames are different, ocr is performed on the frame (for skipped frames, the ocr result is the same as the previous frame)
Length of the text is calculated for each frame
This gives a signal where the quantity that varies over time is the length of the text
Various methods have been tried to detect the most informative frame:
1. Simple peak detection algorithm
2. Moving average methods [1]
3. Profit maximization methods (similar to stock trading)
4. Peak prominence methods
