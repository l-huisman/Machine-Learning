import cv2
import numpy as np

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of blue color in HSV
    lower_blue = np.array([90, 50, 50]) 
    upper_blue = np.array([130, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(frame, frame, mask=mask) # 1 1 -> 1, 1 0 -> 0, 0 0 -> 0

    # Display an image
    cv2.imshow("frame", result)

    # Wait for a key to be pressed
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
