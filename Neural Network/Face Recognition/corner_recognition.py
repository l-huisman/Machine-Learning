import os
import cv2
import numpy as np

# Check if the image exists
image_path = "./images/mondrian.png"
if os.path.exists(image_path) == False:
    print("Image not found!")
    exit()

# Read an image
img = cv2.imread("images/mondrian.png")

# Half the size of the image
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5) # type: ignore

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Show the grayscale image
cv2.imshow("Grayscale", gray)

# Detect corners
corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10) # 100: max corners, 0.01: quality, 10: min distance

# Convert to integers
corners = np.int0(corners) # type: ignore

# Draw circles around the corners
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x, y), 5, (0, 0, 255), 1) # source, center, radius, color, thickness

# Draw lines between the corners
for i in range(len(corners)):
    for j in range(i + 1, len(corners)):
        corner1 = tuple(corners[i][0])
        corner2 = tuple(corners[j][0])
        colour = tuple(map(lambda x: int(x), np.random.randint(0, 255, size=3))) # Map the random numbers to integers because it returns a 32 or 64 bit integer and we need an 8 bit integer
        cv2.line(img, corner1, corner2, colour, 1) # source, point1, point2, color, thickness

# Show the image with the corners
cv2.imshow("Corners", img)

# Wait for a key to be pressed
cv2.waitKey(0)  # 0: wait forever

# Destroy all windows
cv2.destroyAllWindows()