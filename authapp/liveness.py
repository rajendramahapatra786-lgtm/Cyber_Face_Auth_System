import cv2
import numpy as np
import base64
import mediapipe as mp


class LivenessDetector:
    def __init__(self):

        # MediaPipe FaceMesh
        self.mp_face_mesh = mp.solutions.face_mesh

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True
        )

        # Left + Right eye landmark indexes
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    # -----------------------------------------
    # Eye Aspect Ratio calculation
    # -----------------------------------------
    def eye_aspect_ratio(self, eye_points, landmarks, w, h):

        points = []

        for idx in eye_points:
            x = int(landmarks[idx].x * w)
            y = int(landmarks[idx].y * h)
            points.append((x, y))

        # vertical distances
        A = np.linalg.norm(
            np.array(points[1]) - np.array(points[5])
        )

        B = np.linalg.norm(
            np.array(points[2]) - np.array(points[4])
        )

        # horizontal distance
        C = np.linalg.norm(
            np.array(points[0]) - np.array(points[3])
        )

        ear = (A + B) / (2.0 * C)

        return ear

    # -----------------------------------------
    # Detect blink in single frame
    # -----------------------------------------
    def detect_blink_in_frame(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            print("No face detected")
            return False

        landmarks = results.multi_face_landmarks[0].landmark

        h, w, _ = frame.shape

        left_ear = self.eye_aspect_ratio(
            self.LEFT_EYE,
            landmarks,
            w,
            h
        )

        right_ear = self.eye_aspect_ratio(
            self.RIGHT_EYE,
            landmarks,
            w,
            h
        )

        avg_ear = (left_ear + right_ear) / 2

        print("EAR:", avg_ear)

        # eye closed threshold
        if avg_ear < 0.22:
            return True
        else:
            return False

    # -----------------------------------------
    # Main liveness check
    # -----------------------------------------
    def check_liveness_and_count_blinks(self, frames_data):

        blink_count = 0
        was_blinking = False

        frames_decoded = []

        # Decode frames
        for frame_b64 in frames_data:

            if ',' in frame_b64:
                frame_b64 = frame_b64.split(',')[1]

            frame_bytes = base64.b64decode(frame_b64)

            nparr = np.frombuffer(
                frame_bytes,
                np.uint8
            )

            frame = cv2.imdecode(
                nparr,
                cv2.IMREAD_COLOR
            )

            if frame is not None:
                frames_decoded.append(frame)

        if len(frames_decoded) == 0:
            return 0, False

        # Check every frame
        for frame in frames_decoded:

            try:

                is_blinking = self.detect_blink_in_frame(
                    frame
                )

                # Count transition open -> closed
                if is_blinking and not was_blinking:

                    blink_count += 1

                    print(
                        f"BLINK DETECTED = {blink_count}"
                    )

                was_blinking = is_blinking

            except Exception as e:

                print("Frame error:", e)
                continue

        print("Final Blink Count:", blink_count)

        if blink_count >= 2:
            return blink_count, True
        else:
            return blink_count, False