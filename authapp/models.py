from django.db import models
from django.contrib.auth.models import User


class LoginActivity(models.Model):
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('UNKNOWN_FACE', 'Unknown Face'),
        ('LIVENESS_FAILED', 'Liveness Failed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    login_time = models.DateTimeField(auto_now_add=True)

    logout_time = models.DateTimeField(
        null=True,
        blank=True
    )

    ip_address = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    device_info = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES
    )

    face_image = models.ImageField(
        upload_to='login_faces/',
        null=True,
        blank=True
    )

    session_duration = models.DurationField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user} - {self.status}"