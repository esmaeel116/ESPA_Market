from rest_framework import serializers
from .models import OTPCode
import random
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

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


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        phone = data['phone_number']
        code = data['code']

        try:
            otp = OTPCode.objects.get(phone_number=phone, code=code)
        except OTPCode.DoesNotExist:
            raise serializers.ValidationError("Invalid code.")

        if otp.is_verified:
            raise serializers.ValidationError("This code has already been used.")

        if otp.is_expired():
            raise serializers.ValidationError("Code has expired.")

        return data

    def create(self, validated_data):
        phone = validated_data['phone_number']
        otp = OTPCode.objects.get(phone_number=phone)

        otp.is_verified = True
        otp.save()

        user, created = User.objects.get_or_create(username=phone)

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
            'username': user.username,
        }