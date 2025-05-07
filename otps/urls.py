from django.urls import path
from .views import OTPRequestView

urlpatterns = [
    path('send/', OTPRequestView.as_view(), name='otp-request'),
]
