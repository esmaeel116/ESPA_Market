from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('R', 'RatherNotToSay'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=20, unique=True)
    phone_verified = models.BooleanField(default=False)
    address = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    profile_image = models.ImageField(upload_to='customers/profiles/', null=True, blank=True)
    loyalty_points = models.PositiveIntegerField(default=0)
    newsletter_subscribed = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} ({self.phone})'
