import cv2
import os
import numpy as np
from PIL import Image

# Path to dataset folder
dataset_path = 'dataset'

# Initialize recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(r'C:\Digital Trust\haarcascades\haarcascade_frontalface_default.xml')  # Update if needed

def get_images_and_labels(path):
    image_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("jpg") or file.endswith("png"):
                image_paths.append(os.path.join(root, file))

    face_samples = []
    ids = []
    label_dict = {}  # Map IDs to names
    current_id = 0

    for image_path in image_paths:
        # Extract label from folder name
        label = os.path.basename(os.path.dirname(image_path))

        if label not in label_dict:
            label_dict[label] = current_id
            current_id += 1

        id_ = label_dict[label]

        pil_img = Image.open(image_path).convert("L")  # Convert to grayscale
        img_numpy = np.array(pil_img, "uint8")

        faces = face_cascade.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id_)

    return face_samples, ids, label_dict

print("📚 Training in progress...")
faces, ids, label_map = get_images_and_labels(dataset_path)
recognizer.train(faces, np.array(ids))

# Save model and label mapping
recognizer.save("trainer.yml")

# Save label names for future reference
with open("labels.txt", "w") as f:
    for name, idx in label_map.items():
        f.write(f"{idx}:{name}\n")

print("✅ Training complete. Model saved as 'trainer.yml' and labels as 'labels.txt'")
