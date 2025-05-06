from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.select_related('customer')\
            .prefetch_related('items__product')\
            .filter(customer__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.select_related('order', 'product')\
            .filter(order__customer__user=self.request.user)
