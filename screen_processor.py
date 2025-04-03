import cv2
import numpy as np
from PIL import ImageGrab

def capture_window(region):
    img = ImageGrab.grab(bbox=(
        region['left'], 
        region['top'],
        region['left'] + region['width'],
        region['top'] + region['height']
    ))
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def find_template(screenshot, template_path, threshold=0.8):
    template = cv2.imread(template_path)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val > threshold:
        h, w = template.shape[:-1]
        return (max_loc[0] + w//2, max_loc[1] + h//2)
    return None
