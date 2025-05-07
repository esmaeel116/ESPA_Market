from rest_framework import serializers
from .models import Customer
from django.contrib.auth.models import User


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CustomerSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address']
