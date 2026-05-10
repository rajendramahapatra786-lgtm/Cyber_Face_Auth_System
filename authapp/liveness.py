import cv2
import numpy as np
import base64

class LivenessDetector:
    def __init__(self):
        # Load face and eye cascades (built into OpenCV)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
        
    def detect_eyes_in_frame(self, frame):
        """Detect eyes and return if eyes are open or closed"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect face first
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return False, 0  # No face detected
        
        # Get the first face
        (x, y, w, h) = faces[0]
        roi_gray = gray[y:y+h, x:x+w]
        
        # Detect eyes within face region
        eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
        
        # If 0 or 1 eye detected, could be blinking or eyes closed
        eyes_detected = len(eyes)
        
        # If eyes are closed (0 eyes detected) - counts as blink frame
        is_blinking = eyes_detected < 2
        
        return is_blinking, eyes_detected
    
    def check_liveness_and_count_blinks(self, frames_data):
        """Check multiple frames for blink pattern"""
        blink_count = 0
        was_blinking = False
        frames_decoded = []
        
        # Decode all frames
        for frame_b64 in frames_data:
            if ',' in frame_b64:
                frame_b64 = frame_b64.split(',')[1]
            frame_bytes = base64.b64decode(frame_b64)
            nparr = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is not None:
                frames_decoded.append(frame)
        
        if len(frames_decoded) == 0:
            return 0, False
        
        # Analyze each frame for blink pattern
        for frame in frames_decoded:
            try:
                is_blinking, eyes_count = self.detect_eyes_in_frame(frame)
                
                # Count blinks (transition from open -> closed)
                if is_blinking and not was_blinking:
                    blink_count += 1
                    print(f"Blink detected! Total: {blink_count}")
                
                was_blinking = is_blinking
            except Exception as e:
                print(f"Error processing frame: {e}")
                continue
        
        print(f"Total blinks detected: {blink_count}")
        
        if blink_count >= 2:
            return blink_count, True
        else:
            return blink_count, False