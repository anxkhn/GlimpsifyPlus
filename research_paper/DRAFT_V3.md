#### **4. Methodology**

- **4.1 Video Processing Pipeline**:
  - open cv is used for ingesting video in the intervals of 3 seconds
- **4.2 Frame Comparison Algorithm**:

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

- A 0.5 percent threshold is found to work empirically. We ran a qualitative experiment to check which threshold works the best. And the type of educational videos we worked with, 0.5 percent threshold works empirically well.
- Example of images equal or not equal
- ![alt text](image.png)
- **4.3 Text Extraction and Signal Generation**:
  - OCR is performed for each of the ingested frames
  - The character count of the extracted text from the OCR is saved frame by frame thus generating a temporal signal of variation in character count
  - For the frames that were found almost equal, the OCR result of previously processed frames were used, thus saving time and computational resources required to perform OCR
- **4.4 Key Frame Selection Methods**:
    - For selecting the key frames we are making analogy with stock trading and re thinking the original problem statement as the following: 𝘔𝘢𝘹𝘪𝘮𝘪𝘻𝘦 𝘗𝘳𝘰𝘧𝘪𝘵 𝘣𝘺 𝘉𝘶𝘺𝘪𝘯𝘨 𝘢𝘯𝘥 𝘚𝘦𝘭𝘭𝘪𝘯𝘨 𝘢 𝘚𝘵𝘰𝘤𝘬 𝘢𝘵 𝘮𝘰𝘴𝘵 𝘒 𝘛𝘪𝘮𝘦𝘴
    - The selling of a stock is analogous to the key frame selection process, where we are selling the stock at the peak price
    - The buying of a stock makes sure that only one key frame is selected in one up trend
    - The K times of buying and selling is the number of key frames we are selecting from the video
    - Since the number of key frames to find, that is K, is not known, we are using peak prominence method to find the approximate number of key frames in the video and use that as K
