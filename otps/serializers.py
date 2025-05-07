from rest_framework import serializers
from .models import OTPCode
import random


class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def create(self, validated_data):
        phone = validated_data['phone_number']
        code = str(random.randint(1000, 9999))

        otp, created = OTPCode.objects.update_or_create(
            phone_number=phone,
            defaults={'code': code, 'is_verified': False}
        )

        print(f"[OTP] Code for {phone}: {code}")

        return otp
