from django.urls import path
from . import views

urlpatterns = [
    path('verify/', views.verify_face, name='verify_face'),
    path('register/', views.register_face, name='register_face'),

]