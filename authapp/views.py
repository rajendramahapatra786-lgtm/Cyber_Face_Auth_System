import json
import base64
import cv2
import numpy as np

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .face_utils import CyberFaceRecognizer
from .liveness import LivenessDetector
from .face_validation import FaceValidator

import os
from django.conf import settings


from .models import LoginActivity
from django.core.files.base import ContentFile



face_recognizer = CyberFaceRecognizer()
liveness_detector = LivenessDetector()
face_validator = FaceValidator()




# Failed login counter
failed_attempts = 0


def get_client_ip(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


@csrf_exempt
@require_http_methods(["POST"])
def verify_face(request):
    """
    Original face verify endpoint
    """

    try:
        data = json.loads(request.body)

        image_data = data.get('image', '')

        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]

        image_bytes = base64.b64decode(image_data)

        name, confidence = face_recognizer.detect_and_recognize(image_bytes)

        if name:
            return JsonResponse({
                'status': 'success',
                'name': name.title(),
                'confidence': float(confidence)
            })

        else:
            return JsonResponse({
                'status': 'fail',
                'message': 'Face not recognized'
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def verify_with_liveness_first(request):
    """
    Step 1 → Blink detection
    Step 2 → Full face validation
    Step 3 → Face recognition
    """

    global failed_attempts

    device_info = request.META.get('HTTP_USER_AGENT')

    try:
        print("=" * 50)
        print("Received request to verify-with-liveness")

        data = json.loads(request.body)

        frames = data.get('frames', [])

        print(f"Number of frames received: {len(frames)}")

        # Need enough frames
        if len(frames) < 5:
            return JsonResponse({
                'status': 'error',
                'message': f'Need at least 5 frames, got {len(frames)}'
            }, status=400)

        # ---------------------------------------------------
        # STEP 1 → LIVENESS CHECK
        # ---------------------------------------------------

        blink_count, is_live = liveness_detector.check_liveness_and_count_blinks(frames)

        print(f"Blink count: {blink_count}, Is live: {is_live}")

        


        if not is_live:

            LoginActivity.objects.create(
                ip_address=get_client_ip(request),
                device_info=device_info,
                status='LIVENESS_FAILED'
            )

            return JsonResponse({
                'status': 'fail',
                'message': f'BLINK FAILED: Only {blink_count} blink(s) detected. Need 2 blinks.',
                'blink_count': blink_count,
                'liveness_failed': True
            })

        # ---------------------------------------------------
        # STEP 2 → GET LAST FRAME
        # ---------------------------------------------------

        last_frame = frames[-1]

        if ',' in last_frame:
            last_frame = last_frame.split(',')[1]

        image_bytes = base64.b64decode(last_frame)

        # Convert bytes → OpenCV image
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # ---------------------------------------------------
        # STEP 3 → FULL FACE VALIDATION
        # ---------------------------------------------------

        valid_face, validation_message = face_validator.is_face_fully_visible(frame)

        print("Face Validation:", validation_message)

        if not valid_face:
            return JsonResponse({
                'status': 'fail',
                'message': validation_message
            })

        # ---------------------------------------------------
        # STEP 4 → FACE RECOGNITION
        # ---------------------------------------------------

        name, confidence = face_recognizer.detect_and_recognize(image_bytes)

        # =========================
        # FACE MATCH SUCCESS
        # =========================

        if name:

            # Reset failed attempts
            failed_attempts = 0

            LoginActivity.objects.create(
    user=None,
    ip_address=get_client_ip(request),
    device_info=device_info,
    status='SUCCESS'
)

            return JsonResponse({
                'status': 'success',
                'name': name.title(),
                'confidence': float(confidence),
                'blink_count': blink_count,
                'message': f'✅ {blink_count} blinks detected - Face matched!'
            })

        # =========================
        # FACE MATCH FAILED
        # =========================

        else:

            failed_attempts += 1

            LoginActivity.objects.create(
    ip_address=get_client_ip(request),
    device_info=device_info,
    status='FAILED'
)

            print(f"Failed Attempts: {failed_attempts}")

            # 1st Failed Attempt
            if failed_attempts == 1:

                return JsonResponse({
                    'status': 'fail',
                    'message': '⚠ Face not recognized. Please try again.',
                    'blink_count': blink_count
                })

            # 2nd Failed Attempt
            elif failed_attempts == 2:

                save_intruder_image(frame, request)
                return JsonResponse({
                    'status': 'fail',
                    'message': '📸 Unauthorized face detected. Intruder image captured.',
                    'blink_count': blink_count
                })

            # 3rd Failed Attempt
            elif failed_attempts >= 3:

                save_intruder_image(frame, request)

                return JsonResponse({
                    'status': 'fail',
                    'message': '🚫 System temporarily locked due to multiple failed attempts.',
                    'blink_count': blink_count
                })

    except json.JSONDecodeError as e:

        print(f"JSON Decode Error: {e}")

        return JsonResponse({
            'status': 'error',
            'message': f'Invalid JSON: {str(e)}'
        }, status=400)

    except Exception as e:

        print(f"General Error: {e}")

        import traceback
        traceback.print_exc()

        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def register_face(request):

    try:
        data = json.loads(request.body)

        images = data.get('images', [])
        username = data.get('username', 'user')

        for i, img_data in enumerate(images):

            if 'base64,' in img_data:
                img_data = img_data.split('base64,')[1]

            image_bytes = base64.b64decode(img_data)

            file_path = face_recognizer.known_faces_dir / f"{username}_{i}.jpg"

            with open(file_path, 'wb') as f:
                f.write(image_bytes)

        # Reload embeddings
        face_recognizer.load_known_faces()

        return JsonResponse({
            'status': 'success',
            'message': 'Face Registered Successfully'
        })

    except Exception as e:

        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


# ===================================================
# SAVE INTRUDER IMAGE
# ===================================================

def save_intruder_image(frame, request):

    intruder_folder = os.path.join(
        settings.MEDIA_ROOT,
        'intruders'
    )

    os.makedirs(intruder_folder, exist_ok=True)

    image_count = len(os.listdir(intruder_folder)) + 1

    filename = f"intruder_{image_count}.jpg"

    image_path = os.path.join(
        intruder_folder,
        filename
    )

    cv2.imwrite(image_path, frame)

    print(f"Intruder image saved: {image_path}")

    # =========================
    # SAVE TO LOGIN ACTIVITY
    # =========================

    activity = LoginActivity.objects.create(
        ip_address=get_client_ip(request),
        device_info=request.META.get('HTTP_USER_AGENT'),
        status='UNKNOWN_FACE'
    )

    with open(image_path, 'rb') as f:

        activity.face_image.save(
            filename,
            ContentFile(f.read()),
            save=True
        )