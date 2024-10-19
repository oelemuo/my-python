"""
This file will convert a colored image RGB into a grayscale image
The program will load a color image, use NumPy to average the RGB values for each pixel,
creating a single grayscale value and saving it.
"""

import numpy as np
import cv2
# function converting image to grayscale for ML model to understand
def convert_to_grayscale(image_path):
    image = cv2.imread(image_path) # loads image
    # need to average the RGB channels to convert to grayscale
    grayscale_image = np.mean(image, axis=2).astype(np.uint8) # Averages across channels

    # Save the grayscale image
    cv2.imwrite(r'C:\Users\obinn\Desktop\brightened_image.jpg', grayscale_image)
    return grayscale_image

#example usage
convert_to_grayscale(r'C:\Users\obinn\Desktop\brightened_image.jpg')