from django.urls import path
from .views import OTPRequestView, OTPVerifyView

urlpatterns = [
    path('send/', OTPRequestView.as_view(), name='otp-request'),
    path('verify/', OTPVerifyView.as_view(), name='otp-verify'),
]
