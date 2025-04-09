import cv2

# Load Haar Cascade (Use the full path)
face_cascade = cv2.CascadeClassifier(r'C:\Digital Trust\haarcascades\haarcascade_frontalface_default.xml')

# Debugging: Check if the file is loaded
if face_cascade.empty():
    print("Error: Haar Cascade file not found or could not be loaded!")
    exit()  # Stop the program if the file is not found
else:
    print("✅ Haar Cascade loaded successfully!")

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open the camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
