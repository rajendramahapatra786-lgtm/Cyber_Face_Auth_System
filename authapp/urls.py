from django.urls import path
from . import views

urlpatterns = [
    path('verify/', views.verify_face, name='verify_face'),
    path('verify-liveness/', views.verify_with_liveness_first, name='verify_liveness'),  # NEW
    path('register/', views.register_face, name='register_face'),
]