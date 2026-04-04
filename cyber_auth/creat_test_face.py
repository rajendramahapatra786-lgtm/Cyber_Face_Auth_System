"""
Create a test face image for the Cyber Face Auth System
Run this script to create a sample face for testing
"""

import cv2
import numpy as np
import os

def create_test_face():
    """Create a synthetic test face image"""
    
    # Create output directory if it doesn't exist
    output_dir = 'authapp/known_faces'
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a blank image (300x300)
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    
    # Fill with skin tone color
    img[:] = [200, 180, 150]  # BGR format - skin tone
    
    # Draw face outline (oval)
    cv2.ellipse(img, (150, 150), (80, 100), 0, 0, 360, (180, 150, 120), -1)
    
    # Draw eyes
    cv2.circle(img, (115, 130), 12, (50, 50, 50), -1)  # Left eye
    cv2.circle(img, (185, 130), 12, (50, 50, 50), -1)  # Right eye
    
    # Eye pupils
    cv2.circle(img, (115, 130), 5, (0, 0, 0), -1)
    cv2.circle(img, (185, 130), 5, (0, 0, 0), -1)
    
    # Eye highlights
    cv2.circle(img, (110, 125), 3, (255, 255, 255), -1)
    cv2.circle(img, (180, 125), 3, (255, 255, 255), -1)
    
    # Draw nose
    cv2.ellipse(img, (150, 165), (15, 20), 0, 0, 360, (140, 120, 100), -1)
    
    # Draw mouth (smile)
    cv2.ellipse(img, (150, 195), (30, 15), 0, 0, 180, (100, 80, 60), -1)
    
    # Draw eyebrows
    cv2.ellipse(img, (115, 110), (20, 8), 0, 0, 360, (80, 60, 40), -1)
    cv2.ellipse(img, (185, 110), (20, 8), 0, 0, 360, (80, 60, 40), -1)
    
    # Add glasses (optional - cyber look!)
    cv2.rectangle(img, (95, 115), (135, 145), (0, 255, 255), 2)
    cv2.rectangle(img, (165, 115), (205, 145), (0, 255, 255), 2)
    cv2.line(img, (135, 130), (165, 130), (0, 255, 255), 2)
    
    # Add cyber scan lines effect
    for i in range(0, 300, 10):
        cv2.line(img, (0, i), (300, i), (100, 255, 100), 1)
    
    # Save the image
    output_path = os.path.join(output_dir, 'rajendra.jpg')
    cv2.imwrite(output_path, img)
    
    print(f"✓ Test face created successfully!")
    print(f"  Location: {output_path}")
    print(f"  Name: rajendra")
    print(f"\n📌 This is a synthetic test face. For real recognition, replace with actual face photos.")
    
    return output_path

def create_webcam_face(name="rajendra"):
    """Capture a real face from webcam (optional)"""
    
    print(f"\n📷 Option: Capture real face from webcam")
    print("  Press 'SPACE' to capture, 'ESC' to cancel")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("  ✗ Cannot open webcam")
        return None
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    captured = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Show frame
        display = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(display, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(display, "FACE DETECTED", (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.putText(display, "Press SPACE to capture, ESC to cancel", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.imshow('Capture Face - Cyber Auth System', display)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # SPACE
            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_roi = frame[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (300, 300))
                
                output_dir = 'authapp/known_faces'
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f'{name}.jpg')
                cv2.imwrite(output_path, face_roi)
                print(f"✓ Face captured and saved: {output_path}")
                captured = True
                break
            else:
                print("  No face detected! Please position your face in frame.")
        
        elif key == 27:  # ESC
            print("  Capture cancelled")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return output_path if captured else None

if __name__ == "__main__":
    print("=" * 50)
    print("🔷 CYBER FACE AUTH - Setup Tool 🔷")
    print("=" * 50)
    
    print("\nChoose an option:")
    print("1. Create synthetic test face (quick, no camera needed)")
    print("2. Capture real face from webcam")
    print("3. Skip (I'll add my own photos later)")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == '1':
        create_test_face()
    elif choice == '2':
        name = input("Enter name for this face (default: rajendra): ").strip()
        if not name:
            name = "rajendra"
        create_webcam_face(name)
    else:
        print("\n✓ Skipping face creation. Add your own photos to authapp/known_faces/")
    
    print("\n✅ Setup complete! Run 'python manage.py runserver' to start the system.")