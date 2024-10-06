import os
import cv2

from file_utils import *

class Frame:
    def __init__(self, frame_path):
        self.frame_id = int(frame_path.split('_')[-1].split('.')[0])
        self.frame_path = frame_path

class PostProcessor: 
    @staticmethod
    def add_text_to_frames_and_save(input_dir, list_of_files, output_dir):
        frames = [Frame(file) for file in list_of_files]
        frames.sort(key=lambda x: x.frame_id)

        n = len(frames) 
        for i, frame in enumerate(frames):
            frame_path = os.path.join(input_dir, frame.frame_path)
            current_frame = cv2.imread(frame_path)
            
            text = f"Glimpsify {i+1}/{n}" 
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size, _ = cv2.getTextSize(text, font, 0.51, 1)
            text_x = 10
            text_y = current_frame.shape[0] - 10 

            overlay = current_frame.copy()
            
            # Draw the filled rectangle on the overlay image
            cv2.rectangle(overlay, (text_x, text_y - text_size[1] - 10), (text_x + text_size[0], text_y), (85, 26, 58), cv2.FILLED)
            cv2.putText(overlay, text, (text_x, text_y - 5), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Blend the overlay with the original image using alpha blending
            opacity = 0.6
            cv2.addWeighted(overlay, opacity, current_frame, 1 - opacity, 0, current_frame)
            
            output_path = os.path.join(output_dir, frame.frame_path)
            cv2.imwrite(output_path, current_frame)

if __name__ == "__main__":
    input_dir = "data/lrpdqi_profits"
    output_dir = "data/lrpdqi_profits_postprocessed"
    create_directory(output_dir)   
    
    list_of_files = os.listdir(input_dir)
    PostProcessor.add_text_to_frames_and_save(input_dir, list_of_files, output_dir)