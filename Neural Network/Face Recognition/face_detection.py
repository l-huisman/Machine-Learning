import cv2
import numpy as np

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Create a cascade classifier object
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") # This is a pre-trained model
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml") # This is a pre-trained model    

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4) # source, scale factor, min neighbours

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 3) # source, start point, end point, color, thickness
        roi = frame[y:y+h, x:x+w] # Region of interest for the face to detect the eyes
        roi_gray = gray[y:y+h, x:x+w] 
        roi_colour = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 4) # source, scale factor, min neighbours
        for (ex, ey, ew, eh) in eyes:
            cv2.circle(roi_colour, (ex+int(ew/2), ey+int(eh/2)), int((ew+eh)/4), (0, 255, 0), 3) # source, center, radius, color, thickness

    # Show the image
    cv2.imshow("frame", frame)

    # Wait for a key to be pressed
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
