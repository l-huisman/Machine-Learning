import cv2
import numpy as np

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    # Add basic shapes
    img = cv2.line(frame, (0, 0), (width, height), (255, 0, 0), 10)
    img = cv2.line(img, (0, height), (width, 0), (0, 255, 0), 5)
    img = cv2.rectangle(img, (100, 100), (200, 200), (0, 255, 0), 5)
    img = cv2.circle(img, (300, 300), 50, (0, 0, 255), 10)
    img = cv2.putText(img, "Luke is amazing", (100, height-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, cv2.LINE_AA)

    # Display an image
    cv2.imshow("frame", frame)

    # Wait for a key to be pressed
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
