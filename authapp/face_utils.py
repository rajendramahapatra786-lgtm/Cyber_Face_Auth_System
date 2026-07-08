import cv2
import numpy as np
from pathlib import Path


class CyberFaceRecognizer:

    def __init__(self):

        self.known_faces_dir = Path(__file__).parent / "known_faces"
        self.known_faces_dir.mkdir(exist_ok=True)

        # LBPH recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Haarcascade face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        self.label_map = {}

        print("Training face recognizer...")
        self.train_model()

    # ---------------------------------
    # Train all known faces
    # ---------------------------------
    def train_model(self):

        faces = []
        labels = []

        current_label = 0

        for img_path in self.known_faces_dir.glob("*.*"):

            if img_path.suffix.lower() not in [
                ".jpg", ".jpeg", ".png"
            ]:
                continue

            name = img_path.stem.split("_")[0]

            img = cv2.imread(str(img_path))
            gray = cv2.cvtColor(
                img,
                cv2.COLOR_BGR2GRAY
            )

            detected = self.face_cascade.detectMultiScale(
                gray,
                1.3,
                5
            )

            if len(detected) == 0:
                continue

            x, y, w, h = detected[0]

            face_roi = gray[y:y+h, x:x+w]

            faces.append(face_roi)
            labels.append(current_label)

            self.label_map[current_label] = name

            print("Loaded:", name)

            current_label += 1

        if len(faces) > 0:

            self.recognizer.train(
                faces,
                np.array(labels)
            )

            print("Training complete")

        else:
            print("No known faces found")

    # ---------------------------------
    # Recognize current face
    # ---------------------------------
    def detect_and_recognize(
        self,
        image_bytes
    ):

        try:

            nparr = np.frombuffer(
                image_bytes,
                np.uint8
            )

            img = cv2.imdecode(
                nparr,
                cv2.IMREAD_COLOR
            )

            gray = cv2.cvtColor(
                img,
                cv2.COLOR_BGR2GRAY
            )

            faces = self.face_cascade.detectMultiScale(
                gray,
                1.3,
                5
            )

            if len(faces) == 0:
                return None, None

            x, y, w, h = faces[0]

            face_roi = gray[y:y+h, x:x+w]

            label, confidence = self.recognizer.predict(
                face_roi
            )

            print("Confidence:", confidence)

            # Lower confidence = better
            if confidence < 80:

                name = self.label_map[label]

                score = 1 - (confidence / 100)

                return name, score

            return None, None

        except Exception as e:

            print("Recognition Error:", e)

            return None, None