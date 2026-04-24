import cv2
import numpy as np
from pathlib import Path


class CyberFaceRecognizer:
    def __init__(self):
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        self.known_faces_dir = Path(__file__).parent / 'known_faces'
        self.known_faces_dir.mkdir(exist_ok=True)

        self.known_faces = {}
        self.load_known_faces()

    def load_known_faces(self):
        self.known_faces = {}

        for img_path in self.known_faces_dir.glob('*.jpg'):
            # name_0.jpg → name
            name = img_path.stem.split('_')[0]

            img = cv2.imread(str(img_path))
            if img is None:
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_roi = cv2.resize(gray[y:y+h, x:x+w], (100, 100))

                # store multiple faces
                if name not in self.known_faces:
                    self.known_faces[name] = []

                self.known_faces[name].append(face_roi)

                print(f"Loaded: {img_path.name}")

    def detect_and_recognize(self, image_bytes):
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return None, None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return None, None

        # Take largest face
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        face_roi = cv2.resize(gray[y:y+h, x:x+w], (100, 100))

        best_match = None
        best_confidence = 0

        for name, face_list in self.known_faces.items():
            for known_face in face_list:
                result = cv2.matchTemplate(face_roi, known_face, cv2.TM_CCOEFF_NORMED)
                confidence = result[0][0]

                print("Comparing:", name, "Confidence:", confidence)

                if confidence > best_confidence and confidence > 0.5:
                    best_confidence = confidence
                    best_match = name

        return best_match, best_confidence