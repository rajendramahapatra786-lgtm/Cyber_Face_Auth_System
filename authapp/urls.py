from django.urls import path
from . import views

urlpatterns = [
    path('verify/', views.verify_face, name='verify_face'),
    path('verify-liveness/', views.verify_with_liveness_first, name='verify_liveness'),  # NEW
    path('register/', views.register_face, name='register_face'),
    path('security-monitor/',views.security_monitor,name='security_monitor'),
    path('security-monitor/delete/<int:log_id>/',views.delete_log,name='delete_log'),
]