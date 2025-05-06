from rest_framework import serializers
from .models import Discount
from products.models import Product

class DiscountSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = Discount
        fields = ['id', 'product', 'product_title', 'percentage', 'active', 'start_date', 'end_date']
