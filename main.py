import cv2
import numpy as np
import time 

import traceback
from termcolor import colored

class LineTracking:
    def __init__(self, threshold_value=48):
        self.data = { 
            0 : (0,0),
            1 : (1,0),
            2 : (2,0), 
            3 : (0,1),
            4 : (1,1),
            5 : (2,1),
            7 : (1,2),
            6 : (0,2),
            8 : (2,2)
        } 

        self.threshold_value = threshold_value

    def crop_image(
        self, 
        gray_image, 
        w, 
        h, 
        col, 
        row, 
        distance, 
        center_ratio=1
    ):
        try:
            y_start, y_end = row * h, (row + 1) * h
            x_start, x_end = col * w + distance // 2, (col + 1) * w + distance // 2 

            center_height = int(h * center_ratio)
            center_width = int(w * center_ratio)

            center_y_start = y_start + (h - center_height) // 2
            center_y_end = center_y_start + center_height

            center_x_start = x_start + (w - center_width) // 2
            center_x_end = center_x_start + center_width

            center_region = gray_image[center_y_start:center_y_end, center_x_start:center_x_end]

            return center_region
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
        
    def process(
        self,
        frame
    ):
        try:
            total_pixels = frame.size
            black_pixels = np.count_nonzero(frame < self.threshold_value)
            
            black_ratio_percent = (black_pixels / total_pixels) * 100
            return black_ratio_percent
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
    
    def update(
        self, 
        gray_frame
    ): 
        try:
            height, width = gray_frame.shape

            distance = width - height

            h, w = height // 3, (width - distance) // 3

            data = {} 
            
            for region_number,cor in self.data.items():
                piece = self.crop_image(gray_frame,w,h,cor[0],cor[1],distance)
                black_ratio_percent = self.process(piece)
                data[region_number] = int(black_ratio_percent)
              
            return data
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
