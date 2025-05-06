from rest_framework import serializers
from .models import Order, OrderItem, Coupon
from products.models import Product
from customers.models import Customer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'status', 'is_paid', 'items']


# Optional: If you're planning to use coupons in your API
class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_percentage', 'active', 'start_date', 'end_date', 'is_valid']

    def get_is_valid(self, obj):
        return obj.is_valid()
