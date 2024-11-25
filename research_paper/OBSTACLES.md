
## Obstacles faced

1. Simple peak detection algorithm:
   - This method was not robust enough to handle noisy data
   - The algorithm was not able to differentiate between peaks and noise
   - The algorithm was not able to handle multiple peaks in the data
   - The algorithm was not able to handle the case where the most informative frame was not the peak
2. Moving average methods:
   - When the moving average window was small, the peaks that were close to each other were not detected
   - When the moving average window was large, the peaks were smoothed out and the most informative frame was not detected
   - Moving average method also shifted the peaks in the data, which made it difficult to detect the most informative frame
3. Profit maximization methods:
   - Number of trades need to be specified (which equals to the number of peaks in the data, which is same as number of important frames)
   - As it is not possible to know the number of peaks in the data beforehand, this method can't give all the important frames
   - Though this method is able to detect the most informative frames very well, it can only detect a fixed number of frames which we need to specify beforehand
4. Peak prominence methods:
   - This method was able to detect peaks but it required a lot of manual tuning of the parameters namely `prominence` and `width`


