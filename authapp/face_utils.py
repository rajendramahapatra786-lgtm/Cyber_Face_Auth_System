from deepface import DeepFace
from pathlib import Path
import numpy as np
import cv2


class CyberFaceRecognizer:
    def __init__(self):
        self.known_faces_dir = Path(__file__).parent / 'known_faces'
        self.known_faces_dir.mkdir(exist_ok=True)

        self.known_embeddings = []
        self.known_names = []

        print("Loading embeddings...")
        self.load_known_faces()

    # 🔥 STEP 1: Load all embeddings ONCE
    def load_known_faces(self):
        self.known_embeddings = []
        self.known_names = []

        for img_path in self.known_faces_dir.glob('*.*'):
            if img_path.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
                continue

            name = img_path.stem.split('_')[0]

            try:
                embedding = DeepFace.represent(
                    img_path=str(img_path),
                    model_name="Facenet",
                    enforce_detection=False
                )[0]["embedding"]

                self.known_embeddings.append(np.array(embedding))
                self.known_names.append(name)

                print(f"Loaded: {img_path.name}")

            except Exception as e:
                print(f"Error loading {img_path.name}: {e}")

        print("Total embeddings:", len(self.known_embeddings))

    # 🔥 STEP 2: Fast recognition
    def detect_and_recognize(self, image_bytes):
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                return None, None

            # Get embedding for current frame
            embedding = DeepFace.represent(
                img_path=img,
                model_name="Facenet",
                enforce_detection=False
            )[0]["embedding"]

            embedding = np.array(embedding)

            best_match = None
            best_distance = float("inf")

            # Compare with stored embeddings (FAST)
            for i, known_embedding in enumerate(self.known_embeddings):
                distance = np.linalg.norm(known_embedding - embedding)

                print("Distance:", distance)

                if distance < best_distance:
                    best_distance = distance
                    best_match = self.known_names[i]

            # Threshold (important)
            if best_distance < 15:   # tune this later
                confidence = 1 / (1 + best_distance)
                return best_match, confidence

            return None, None

        except Exception as e:
            print("Error:", e)
            return None, None