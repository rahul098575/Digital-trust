import cv2
import numpy as np
from database import create_table, mark_attendance

# Create attendance table if it doesn't exist
create_table()

# Load the trained model and label mappings
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(r"C:\Digital Trust\haarcascades\haarcascade_frontalface_default.xml")

# Load label mappings
labels = {}
with open("labels.txt", "r") as f:
    for line in f:
        id_str, name = line.strip().split(":")
        labels[int(id_str)] = name

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

marked_names = set()

print("🎥 Real-time recognition started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        id_, confidence = recognizer.predict(face_roi)

        if confidence < 70:
            name = labels.get(id_, "Unknown")
            label = f"{name} ({round(100 - confidence)}%)"

            # Mark attendance only once per session
            if name not in marked_names:
                mark_attendance(name)
                marked_names.add(name)
        else:
            label = "Unknown"

        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
