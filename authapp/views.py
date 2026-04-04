from django.shortcuts import render

# Create your views here.
import json
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .face_utils import CyberFaceRecognizer

face_recognizer = CyberFaceRecognizer()

@csrf_exempt
@require_http_methods(["POST"])
def verify_face(request):
    try:
        data = json.loads(request.body)
        image_data = data.get('image', '')
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        image_bytes = base64.b64decode(image_data)
        name, confidence = face_recognizer.detect_and_recognize(image_bytes)
        if name:
            return JsonResponse({'status': 'success', 'name': name.title(), 'confidence': float(confidence)})
        else:
            return JsonResponse({'status': 'fail', 'message': 'Face not recognized'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)