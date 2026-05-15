import cv2
import numpy as np


class FaceValidator:

    def __init__(self):

        self.face_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def is_face_fully_visible(self, frame):

        try:

            h, w, _ = frame.shape

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5
            )

            # No face
            if len(faces) == 0:
                return False, "❌ No face detected"

            # Use first detected face
            x, y, fw, fh = faces[0]

            # -----------------------------------
            # FACE SIZE CHECK
            # -----------------------------------

            if fw < 100:
                return False, "❌ Move closer to camera"

            # -----------------------------------
            # FACE BORDER CHECK
            # -----------------------------------

            margin = 20

            if (
                x < margin or
                y < margin or
                x + fw > w - margin or
                y + fh > h - margin
            ):
                return False, "❌ Face partially visible"

            # -----------------------------------
            # LOWER FACE CHECK
            # -----------------------------------

            lower_face = gray[
                y + fh // 2:y + fh,
                x:x + fw
            ]

            # Average brightness
            brightness = np.mean(lower_face)

            print("Lower face brightness:", brightness)

            # If lower face too dark
            # likely covered by hand/object
            if brightness < 55:
                return False, "❌ Lower face covered"

            # -----------------------------------
            # FACE WIDTH vs HEIGHT CHECK
            # Helps reject weird partial faces
            # -----------------------------------

            ratio = fw / fh

            print("Face ratio:", ratio)

            if ratio < 0.65 or ratio > 1.1:
                return False, "❌ Face angle incorrect"

            return True, "✅ Face fully visible"

        except Exception as e:

            print("Face Validation Error:", e)

            return False, "❌ Face validation failed"