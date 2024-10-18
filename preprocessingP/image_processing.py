import numpy as np # importy for workingn with arrays
import cv2 # import for working with images

# Function which Loads the images using OpenCV
def adjust_brightness(image_path, brightness_value=50):
    image = cv2.imread(image_path) #reads image as a NumPy array
    #This adds brightness to each pixel in the image
    brightened_image = np.clip(image + brightness_value, 0, 255)

    #save the new brightened image
    cv2.imwrite(r'C:\Users\obinn\Desktop\brightened_image.jpg', brightened_image)
    return brightened_image

#example usage
adjust_brightness(r'C:\Users\obinn\Downloads\893dce4ad3ddfdf0c8487c652216590a (1).jpg',50)