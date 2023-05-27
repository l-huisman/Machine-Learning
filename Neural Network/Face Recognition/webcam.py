import cv2
import numpy as np

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()  # ret: boolean, frame: image array
    width = int(cap.get(3))  # 3: width
    height = int(cap.get(4))  # 4: height

    # Create a black canvas
    image = np.zeros(frame.shape, np.uint8)

    # Resize the image to half
    smaller_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # type: ignore

    # Transform the image
    image[: height // 2, : width // 2] = smaller_frame
    image[height // 2 :, : width // 2] = cv2.rotate(smaller_frame, cv2.ROTATE_180)
    image[: height // 2, width // 2 :] = cv2.rotate(smaller_frame, cv2.ROTATE_180)
    image[height // 2 :, width // 2 :] = smaller_frame

    # Display an image
    cv2.imshow("frame", image)

    # Wait for a key to be pressed
    if cv2.waitKey(1) == ord("q"):
        break


# Destroy all windows
cap.release()
cv2.destroyAllWindows()
