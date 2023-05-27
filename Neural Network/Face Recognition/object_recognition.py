import cv2
import numpy as np

# Read in the image and the template to match
img = cv2.imread("images/soccer_practice.jpg")
template = cv2.imread("images/ball.png")

# Half the size of the image and the template
img = cv2.resize(img, (0, 0), fx=0.75, fy=0.75)  # type: ignore
template = cv2.resize(template, (0, 0), fx=0.75, fy=0.75)  # type: ignore


# Get the width, height and channels of the template
height, width, channels = template.shape

# Methods to compare the template to the image
methods = [
    cv2.TM_CCOEFF,
    cv2.TM_CCOEFF_NORMED,
    cv2.TM_CCORR,
    cv2.TM_CCORR_NORMED,
    cv2.TM_SQDIFF,
    cv2.TM_SQDIFF_NORMED,
]

# Iterate through the methods
for method in methods:
    # Create a copy of the image
    img2 = img.copy()

    # Match the template using the current method
    result = cv2.matchTemplate(
        img2, template, method
    )  # This will out a matrix of values that represent how well the template matches the image

    # Find the min and max values and their locations
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Determine the top left corner
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc

    # Determine the bottom right corner
    bottom_right = (
        location[0] + width,
        location[1] + height,
    )  # x + width, y + height of the template

    # Draw the red rectangle
    cv2.rectangle(
        img2, location, bottom_right, 255, 5
    )  # source, top left corner, bottom right corner, color, thickness

    # Show the image
    cv2.imshow("Match", img2)

    # Wait for a key to be pressed
    cv2.waitKey(0)

    # Destroy all windows
    cv2.destroyAllWindows()
