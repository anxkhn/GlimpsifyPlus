## Flow of the project

User enters youtube video link
The video is downloaded and split and distributed to multiple replica service

Steps performed at each replica service:
Video is ingested frame by frame
New frame is compared with the previous frame using the following algorithm
If the frames are almost the same, the frame is skipped
If the frames are different, ocr is performed on the frame (for skipped frames, the ocr result is the same as the previous frame)
Length of the text is calculated for each frame
This gives a signal where the quantity that varies over time is the length of the text

After each video segment is processed:
Aggregate the signal to make one long signal for the complete video
Use peak detection algorithm to detect the most informative frames
Extract those frames from the video
Make PDF of those frames
Store it

