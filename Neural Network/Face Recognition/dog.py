import cv2
import os

image_path = "./images/dog.jpg"
if os.path.exists(image_path) == False:
    print("Image not found!")
    exit()

# Load an image
img = cv2.imread(image_path, 1)  # 1: color, 0: grayscale, -1: unchanged

# Display an image
cv2.imshow("Image", img)

# Wait for a key to be pressed
cv2.waitKey(0) # 0: wait forever

# Destroy all windows
cv2.destroyAllWindows()
