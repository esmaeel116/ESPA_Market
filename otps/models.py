from django.db import models
from django.utils import timezone
from datetime import timedelta


class OTPCode(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=1)

    def __str__(self):
        return f"{self.phone_number} - {self.code}"
