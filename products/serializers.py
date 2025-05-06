from rest_framework import serializers
from .models import Product, Category
from discounts.models import Discount
from django.utils import timezone


class ActiveDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'percentage', 'start_date', 'end_date']


class ProductSerializer(serializers.ModelSerializer):
    active_discount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'title', 'slug', 'description',
            'price', 'image', 'is_available', 'created_at',
            'active_discount'
        ]

    def get_active_discount(self, obj):
        now = timezone.now()
        discount = obj.discounts.filter(
            active=True,
            start_date__lte=now,
            end_date__gte=now
        ).first()
        return ActiveDiscountSerializer(discount).data if discount else None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
